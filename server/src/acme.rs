//! Let's Encrypt certificates through rustls-acme, with what it does made visible.
//!
//! rustls-acme renews by itself while its state stream is polled (see [`drive`]): after
//! deploying a certificate it sleeps until two thirds of the certificate's lifetime have passed
//! (30 days before expiry for a 90-day certificate), then orders a new one over TLS-ALPN-01 on
//! the HTTPS port. A failed order is retried after 1 s, 2 s, 4 s, ... doubling up to 2^16 s
//! (about 18 hours), and the current certificate keeps being served meanwhile. Certificates and
//! the account key are cached in `STATE_DIR/acme`, so a restart reuses them.
//!
//! [`ObservedCache`] wraps that cache to note each certificate's validity as it is loaded or
//! stored, for `/api/health` and the logs.

use std::path::PathBuf;
use std::sync::Arc;
use std::time::Duration;

use async_trait::async_trait;
use parking_lot::RwLock;
use rustls_acme::caches::DirCache;
use rustls_acme::{AccountCache, AcmeState, CertCache, EventError, EventOk};
use serde::Serialize;
use tokio_stream::StreamExt;

/// The certificate being served.
#[derive(Clone, Debug, PartialEq, Eq, Serialize)]
pub struct Certificate {
    pub domains: Vec<String>,
    /// When it expires, in Unix milliseconds.
    pub expires_at: i64,
    /// When it was issued, in Unix milliseconds.
    #[serde(skip)]
    pub issued_at: i64,
}

impl Certificate {
    /// When rustls-acme orders the next one: two thirds into the validity period.
    pub fn renews_at(&self) -> i64 {
        self.expires_at - (self.expires_at - self.issued_at) / 3
    }
}

/// The certificate in use, shared with `/api/health`; `None` until one is loaded or issued
/// (and always for plain HTTP).
pub type CertificateSlot = Arc<RwLock<Option<Certificate>>>;

/// rustls-acme's directory cache, noting the validity of every certificate that passes.
pub struct ObservedCache {
    inner: DirCache<PathBuf>,
    slot: CertificateSlot,
}

impl ObservedCache {
    pub fn new(dir: PathBuf, slot: CertificateSlot) -> Self {
        Self {
            inner: DirCache::new(dir),
            slot,
        }
    }

    fn observe(&self, domains: &[String], pem: &[u8]) {
        if let Some((issued_at, expires_at)) = validity(pem) {
            *self.slot.write() = Some(Certificate {
                domains: domains.to_vec(),
                expires_at,
                issued_at,
            });
        }
    }
}

#[async_trait]
impl CertCache for ObservedCache {
    type EC = std::io::Error;

    async fn load_cert(
        &self,
        domains: &[String],
        directory_url: &str,
    ) -> Result<Option<Vec<u8>>, Self::EC> {
        let pem = self.inner.load_cert(domains, directory_url).await?;
        if let Some(pem) = &pem {
            self.observe(domains, pem);
        }
        Ok(pem)
    }

    async fn store_cert(
        &self,
        domains: &[String],
        directory_url: &str,
        cert: &[u8],
    ) -> Result<(), Self::EC> {
        self.observe(domains, cert);
        self.inner.store_cert(domains, directory_url, cert).await
    }
}

#[async_trait]
impl AccountCache for ObservedCache {
    type EA = std::io::Error;

    async fn load_account(
        &self,
        contact: &[String],
        directory_url: &str,
    ) -> Result<Option<Vec<u8>>, Self::EA> {
        self.inner.load_account(contact, directory_url).await
    }

    async fn store_account(
        &self,
        contact: &[String],
        directory_url: &str,
        account: &[u8],
    ) -> Result<(), Self::EA> {
        self.inner
            .store_account(contact, directory_url, account)
            .await
    }
}

/// The issue and expiry times (Unix milliseconds) of the first certificate in a PEM bundle
/// (rustls-acme stores the private key first, then the chain, leaf first).
pub fn validity(pem: &[u8]) -> Option<(i64, i64)> {
    let leaf = pem::parse_many(pem)
        .ok()?
        .into_iter()
        .find(|p| p.tag() == "CERTIFICATE")?;
    let (_, cert) = x509_parser::parse_x509_certificate(leaf.contents()).ok()?;
    let validity = cert.validity();
    Some((
        validity.not_before.timestamp() * 1000,
        validity.not_after.timestamp() * 1000,
    ))
}

/// The wait rustls-acme applies after the `failures`-th failed order in a row (from 1).
pub fn retry_delay(failures: u32) -> Duration {
    Duration::from_secs(1 << failures.saturating_sub(1).min(16))
}

/// Polls rustls-acme's state for as long as the server runs (it does nothing unless polled)
/// and logs what happens: deployments and renewals at info, failures at warn or error with the
/// next attempt.
pub async fn drive(mut state: AcmeState<std::io::Error, std::io::Error>, slot: CertificateSlot) {
    let mut failures = 0;
    while let Some(event) = state.next().await {
        let current = slot.read().clone();
        let describe = |c: &Certificate| {
            format!(
                "for {}, expires {}, renewal due {}",
                c.domains.join(", "),
                when(c.expires_at),
                when(c.renews_at())
            )
        };
        match event {
            Ok(EventOk::DeployedCachedCert) => {
                if let Some(c) = &current {
                    tracing::info!("acme: serving the cached certificate {}", describe(c));
                }
            }
            Ok(EventOk::DeployedNewCert) => {
                failures = 0;
                if let Some(c) = &current {
                    tracing::info!("acme: issued and deployed a certificate {}", describe(c));
                }
            }
            Ok(EventOk::CertCacheStore | EventOk::AccountCacheStore) => {}
            Err(EventError::Order(error)) => {
                failures += 1;
                let delay = retry_delay(failures);
                let serving = current.as_ref().map_or_else(
                    || "no certificate yet".to_owned(),
                    |c| format!("still serving the one that expires {}", when(c.expires_at)),
                );
                tracing::error!(
                    "acme: certificate order failed ({failures} in a row): {error}; \
                     retrying in {} s, {serving}",
                    delay.as_secs()
                );
            }
            Err(error) => tracing::warn!("acme: {error}"),
        }
    }
}

fn when(ms: i64) -> String {
    jiff::Timestamp::from_millisecond(ms).map_or_else(|_| ms.to_string(), |t| t.to_string())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn mirrors_the_libraries_backoff() {
        let delays: Vec<u64> = [1, 2, 3, 17, 40]
            .into_iter()
            .map(|n| retry_delay(n).as_secs())
            .collect();
        assert_eq!(delays, [1, 2, 4, 65_536, 65_536]);
    }

    #[test]
    fn renews_two_thirds_into_the_validity() {
        let day = 86_400_000;
        let c = Certificate {
            domains: vec![],
            issued_at: 0,
            expires_at: 90 * day,
        };
        assert_eq!(c.renews_at(), 60 * day);
    }

    #[test]
    fn reads_the_leaf_validity_after_the_key() {
        // A 90-day self-signed certificate after a (dummy) key, as rustls-acme stores them.
        let bundle = format!(
            "-----BEGIN PRIVATE KEY-----\nAAAA\n-----END PRIVATE KEY-----\n{}",
            include_str!("../testdata/leaf.pem")
        );
        let (issued, expires) = validity(bundle.as_bytes()).expect("parsed");
        assert_eq!(expires - issued, 90 * 86_400_000);
        assert_eq!(issued, 1_794_281_186_000);
        assert_eq!(validity(b"not pem"), None);
    }
}
