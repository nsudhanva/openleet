//! Enforces the CPU and wall-clock limits on a running child from outside it.

use std::sync::Arc;
use std::sync::atomic::{AtomicU8, Ordering};
use std::time::{Duration, Instant};

const POLL: Duration = Duration::from_millis(10);

/// Why the watchdog killed the child, if it did.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
#[repr(u8)]
pub enum Kill {
    None = 0,
    Cpu = 1,
    Wall = 2,
    /// Killed on purpose after an answer was already judged wrong.
    Early = 3,
}

/// Shared between the watchdog task and the job runner.
#[derive(Clone, Default)]
pub struct KillSwitch(Arc<AtomicU8>);

impl KillSwitch {
    pub fn reason(&self) -> Kill {
        match self.0.load(Ordering::Acquire) {
            1 => Kill::Cpu,
            2 => Kill::Wall,
            3 => Kill::Early,
            _ => Kill::None,
        }
    }

    /// Records `reason` unless one is already set; true when this call set it.
    pub fn claim(&self, reason: Kill) -> bool {
        self.0
            .compare_exchange(
                Kill::None as u8,
                reason as u8,
                Ordering::AcqRel,
                Ordering::Acquire,
            )
            .is_ok()
    }

    /// Kills the child's whole process group; the first reason wins.
    pub fn kill(&self, pid: i32, reason: Kill) {
        if self.claim(reason) {
            // SAFETY: plain syscalls on a pid we started; a stale pid only yields ESRCH.
            unsafe {
                libc::kill(-pid, libc::SIGKILL);
                libc::kill(pid, libc::SIGKILL);
            }
        }
    }
}

/// User plus system CPU ticks from the text of `/proc/<pid>/stat`.
fn cpu_ticks(stat: &str) -> Option<u64> {
    // Fields after the command name, which may itself contain spaces or parentheses.
    let mut fields = stat.rsplit_once(')')?.1.split_whitespace();
    let utime: u64 = fields.nth(11)?.parse().ok()?;
    let stime: u64 = fields.next()?.parse().ok()?;
    Some(utime + stime)
}

/// Clock ticks per second, the unit of `/proc/<pid>/stat` times.
fn ticks_per_second() -> u64 {
    // SAFETY: sysconf has no preconditions.
    let ticks = unsafe { libc::sysconf(libc::_SC_CLK_TCK) };
    // Linux's USER_HZ is 100 everywhere; sysconf only fails on a broken libc.
    u64::try_from(ticks).ok().filter(|&t| t > 0).unwrap_or(100)
}

/// Watches `pid` until it exits or breaks a limit; meant to run as its own task.
pub async fn watch(pid: i32, cpu_limit_ms: u64, wall: Duration, switch: KillSwitch) {
    let started = Instant::now();
    let ticks = ticks_per_second();
    let path = format!("/proc/{pid}/stat");
    loop {
        tokio::time::sleep(POLL).await;
        // Unreadable once the zygote has reaped the child.
        let Some(used) = std::fs::read_to_string(&path)
            .ok()
            .and_then(|s| cpu_ticks(&s))
        else {
            return;
        };
        if used * 1000 / ticks > cpu_limit_ms {
            switch.kill(pid, Kill::Cpu);
            return;
        }
        if started.elapsed() > wall {
            switch.kill(pid, Kill::Wall);
            return;
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reads_utime_and_stime() {
        let stat = "4242 (python3) S 1 4242 4242 0 -1 4194560 1200 0 0 0 150 25 0 0 20 0 2 0 \
                    123456 1572864000 9000 18446744073709551615";
        assert_eq!(cpu_ticks(stat), Some(175));
    }

    #[test]
    fn command_name_may_hold_parentheses_and_spaces() {
        let stat = "7 (a) b (c d)) R 1 7 7 0 -1 0 0 0 0 0 3 4 0 0 20 0 1 0 1 1 1";
        assert_eq!(cpu_ticks(stat), Some(7));
    }

    #[test]
    fn short_or_garbled_stat_is_none() {
        assert_eq!(cpu_ticks(""), None);
        assert_eq!(cpu_ticks("1 (x) S 1 2 3"), None);
        assert_eq!(cpu_ticks("1 (x) S 1 1 1 0 -1 0 0 0 0 0 abc 4"), None);
    }

    #[test]
    fn first_reason_wins() {
        let switch = KillSwitch::default();
        assert_eq!(switch.reason(), Kill::None);
        assert!(switch.claim(Kill::Cpu));
        assert!(!switch.claim(Kill::Early));
        assert_eq!(switch.clone().reason(), Kill::Cpu);
    }
}
