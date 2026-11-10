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

    /// Kills the child's whole process group; the first reason wins.
    pub fn kill(&self, pid: i32, reason: Kill) {
        if self
            .0
            .compare_exchange(0, reason as u8, Ordering::AcqRel, Ordering::Acquire)
            .is_ok()
        {
            // SAFETY: plain syscalls on a pid we started; a stale pid only yields ESRCH.
            unsafe {
                libc::kill(-pid, libc::SIGKILL);
                libc::kill(pid, libc::SIGKILL);
            }
        }
    }
}

/// CPU time (user + system) of a process so far, from /proc.
pub fn cpu_ms(pid: i32) -> Option<u64> {
    let stat = std::fs::read_to_string(format!("/proc/{pid}/stat")).ok()?;
    // Fields after the command name, which may itself contain spaces or parentheses.
    let mut fields = stat.rsplit_once(')')?.1.split_whitespace();
    let utime: u64 = fields.nth(11)?.parse().ok()?;
    let stime: u64 = fields.next()?.parse().ok()?;
    // SAFETY: sysconf has no preconditions.
    let ticks = u64::try_from(unsafe { libc::sysconf(libc::_SC_CLK_TCK) })
        .ok()?
        .max(1);
    Some((utime + stime) * 1000 / ticks)
}

/// Watches `pid` until it exits or breaks a limit; meant to run as its own task.
pub async fn watch(pid: i32, cpu_limit_ms: u64, wall: Duration, switch: KillSwitch) {
    let started = Instant::now();
    loop {
        tokio::time::sleep(POLL).await;
        let Some(used) = cpu_ms(pid) else { return };
        if used > cpu_limit_ms {
            switch.kill(pid, Kill::Cpu);
            return;
        }
        if started.elapsed() > wall {
            switch.kill(pid, Kill::Wall);
            return;
        }
    }
}
