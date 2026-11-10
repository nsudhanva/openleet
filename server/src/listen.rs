//! Listening sockets: handed over by systemd socket activation when present, else bound here.
//!
//! With socket activation systemd owns the sockets, so a restart drops no connection: new
//! ones queue in the kernel while the old process drains and the new one starts.

use std::collections::HashMap;
use std::net::{SocketAddr, TcpListener};
use std::os::fd::{FromRawFd, OwnedFd, RawFd};

use anyhow::{Context, Result};

/// The first file descriptor systemd passes (`SD_LISTEN_FDS_START`).
const FIRST_FD: RawFd = 3;
/// Names given to unnamed sockets, by position.
const DEFAULT_NAMES: [&str; 2] = ["http", "https"];

/// Sockets passed by systemd, by name (`LISTEN_FDNAMES`).
#[derive(Default)]
pub struct Sockets {
    by_name: HashMap<String, OwnedFd>,
}

/// The descriptors systemd passed to this process, with their names, from the values of
/// `LISTEN_PID`, `LISTEN_FDS` and `LISTEN_FDNAMES`. Empty when they are meant for another
/// process or missing.
fn passed(
    listen_pid: Option<&str>,
    listen_fds: Option<&str>,
    names: Option<&str>,
    pid: u32,
) -> Vec<(String, RawFd)> {
    if listen_pid.and_then(|p| p.parse::<u32>().ok()) != Some(pid) {
        return Vec::new();
    }
    let count: RawFd = listen_fds.and_then(|n| n.parse().ok()).unwrap_or(0);
    let mut names = names.unwrap_or_default().split(':');
    (FIRST_FD..FIRST_FD.saturating_add(count.max(0)))
        .enumerate()
        .map(|(i, fd)| {
            let name = names
                .next()
                .filter(|n| !n.is_empty() && *n != "unknown")
                .or_else(|| DEFAULT_NAMES.get(i).copied())
                .unwrap_or("unknown");
            (name.to_owned(), fd)
        })
        .collect()
}

impl Sockets {
    /// Takes the sockets systemd passed to this process, if any. Call once.
    #[must_use]
    pub fn from_systemd() -> Self {
        let var = |name| std::env::var(name).ok();
        let fds = passed(
            var("LISTEN_PID").as_deref(),
            var("LISTEN_FDS").as_deref(),
            var("LISTEN_FDNAMES").as_deref(),
            std::process::id(),
        );
        let mut by_name = HashMap::new();
        for (name, fd) in fds {
            // SAFETY: systemd passed these descriptors to this process (LISTEN_PID matches),
            // they stay open, and this is the only place that takes ownership of them.
            let fd = unsafe { OwnedFd::from_raw_fd(fd) };
            // A socket unit has one FileDescriptorName for all its sockets: two ports in one
            // unit arrive under the same name, and only one of them would be served.
            if by_name.insert(name.clone(), fd).is_some() {
                tracing::warn!("systemd passed two sockets named {name}; one is unused");
            }
        }
        Self { by_name }
    }

    /// Whether systemd passed any socket.
    #[must_use]
    pub fn activated(&self) -> bool {
        !self.by_name.is_empty()
    }

    /// The socket systemd named `name`, else a new one bound to `fallback`; non-blocking,
    /// ready for tokio.
    ///
    /// # Errors
    /// When binding fails or the socket cannot be made non-blocking.
    pub fn take(&mut self, name: &str, fallback: SocketAddr) -> Result<TcpListener> {
        let listener = match self.by_name.remove(name) {
            Some(fd) => {
                tracing::info!("using the {name} socket from systemd");
                TcpListener::from(fd)
            }
            None => TcpListener::bind(fallback).with_context(|| format!("binding {fallback}"))?,
        };
        listener.set_nonblocking(true)?;
        Ok(listener)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reads_named_sockets_meant_for_this_process() {
        assert_eq!(
            passed(Some("42"), Some("2"), Some("http:https"), 42),
            [("http".to_owned(), 3), ("https".to_owned(), 4)]
        );
        assert_eq!(
            passed(Some("42"), Some("2"), Some("https:http"), 42),
            [("https".to_owned(), 3), ("http".to_owned(), 4)]
        );
        // Unnamed sockets are http, then https.
        assert_eq!(
            passed(Some("42"), Some("1"), None, 42),
            [("http".to_owned(), 3)]
        );
        // Another process's sockets, or none at all, are not ours.
        assert_eq!(
            passed(Some("7"), Some("2"), Some("http:https"), 42).len(),
            0
        );
        assert_eq!(passed(None, None, None, 42).len(), 0);
        assert_eq!(passed(Some("42"), Some("-1"), None, 42).len(), 0);
    }
}
