//! Accounts and sessions: password hashes, session cookies, the one-time setup code for the
//! first admin, limits on sign-in attempts, and the middleware that names the signed-in
//! account on each request.
//!
//! - Passwords are hashed with Argon2id (OWASP's parameters: 19 MiB, 2 passes, 1 lane) and a
//!   random salt; at most [`HASHING_AT_ONCE`] hashes run at once, so sign-in floods cannot
//!   exhaust memory.
//! - A session is a random 256-bit token in an `HttpOnly`, `SameSite=Lax` cookie (`Secure` and
//!   `__Host-` over HTTPS). The database keeps only its SHA-256. A session ends 30 days after
//!   its last day of use, at sign-out, or when the account's password changes elsewhere.
//! - Writes from another site are refused (`Origin` and `Sec-Fetch-Site` checks), on top of
//!   `SameSite` cookies and JSON-only bodies.
//! - The setup code is written to `STATE_DIR/setup-code` (mode 0600) while there is no first
//!   admin. Signing up with it makes user 1: the admin, who owns the progress from before
//!   accounts. Until then nobody else can sign up.

use std::collections::{HashMap, HashSet};
use std::net::{IpAddr, SocketAddr};
use std::path::{Path, PathBuf};
use std::sync::Arc;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};

use anyhow::{Context, Result};
use argon2::password_hash::{PasswordHasher, PasswordVerifier};
use argon2::{Algorithm, Argon2, Params, Version};
use axum::extract::{ConnectInfo, FromRequestParts, Request, State};
use axum::http::request::Parts;
use axum::http::{HeaderMap, HeaderValue, Method, header};
use axum::middleware::Next;
use axum::response::{IntoResponse, Response};
use base64::Engine as _;
use base64::engine::general_purpose::URL_SAFE_NO_PAD;
use parking_lot::{Mutex, RwLock};
use sha2::{Digest, Sha256};
use subtle::ConstantTimeEq;

use crate::db::{Store, StoredSession, User, UserId};
use crate::error::{ApiError, ApiResult};
use crate::state::{Learner, Shared, now_ms};

const DAY_MS: i64 = 24 * 60 * 60 * 1000;
/// A session ends this long after its last day of use.
pub const SESSION_MS: i64 = 30 * DAY_MS;
/// A session in use is moved on at most once a day, so reads do not each write.
const RENEW_AFTER_MS: i64 = DAY_MS;
/// Sessions kept per account; signing in again ends the oldest.
pub const MAX_SESSIONS: usize = 20;
/// Accounts a server takes; sign-up refuses more.
pub const MAX_USERS: usize = 10_000;
/// Password length, in characters (NIST SP 800-63B: at least 8, at least 64 allowed).
pub const MIN_PASSWORD: usize = 8;
pub const MAX_PASSWORD: usize = 128;
/// The longest email address SMTP allows.
const MAX_EMAIL: usize = 254;
/// Password hashes computed at once (19 MiB each).
const HASHING_AT_ONCE: usize = 2;
/// Requests that may wait for a hash; more are refused at once, so a flood of sign-ins cannot
/// hold the server's request slots.
const HASHING_QUEUE: usize = 16;
/// How long a request waits for a hash at most.
const HASHING_WAIT: std::time::Duration = std::time::Duration::from_secs(5);
/// The setup code's file in `STATE_DIR`.
const SETUP_FILE: &str = "setup-code";

/// Argon2id with OWASP's minimum parameters.
fn argon2() -> Argon2<'static> {
    let params = Params::new(19 * 1024, 2, 1, None).expect("valid Argon2 parameters");
    Argon2::new(Algorithm::Argon2id, Version::V0x13, params)
}

/// A password's Argon2id PHC string, with a random salt.
pub fn hash_password(password: &str) -> Result<String> {
    argon2()
        .hash_password(password.as_bytes())
        .map(|hash| hash.to_string())
        .map_err(|e| anyhow::anyhow!("hashing a password: {e}"))
}

/// Whether `password` matches the PHC string `hash` (in constant time).
pub fn verify_password(password: &str, hash: &str) -> bool {
    argon2().verify_password(password.as_bytes(), hash).is_ok()
}

/// `n` random bytes from the operating system.
fn random<const N: usize>() -> [u8; N] {
    let mut bytes = [0; N];
    getrandom::fill(&mut bytes).expect("the operating system's random source");
    bytes
}

fn sha256(bytes: &[u8]) -> [u8; 32] {
    Sha256::digest(bytes).into()
}

/// An email as stored: trimmed and lowercased, or `None` when it is not an address.
pub fn normalize_email(email: &str) -> Option<String> {
    let email = email.trim().to_lowercase();
    let (local, domain) = email.rsplit_once('@')?;
    let valid = !local.is_empty()
        && domain.len() >= 3
        && domain.contains('.')
        && !domain.starts_with('.')
        && !domain.ends_with('.')
        && email.len() <= MAX_EMAIL
        && !email
            .chars()
            .any(|c| c.is_whitespace() || c.is_control() || matches!(c, '<' | '>' | '"'));
    valid.then_some(email)
}

/// Checks a new password's length.
pub fn check_password(password: &str) -> ApiResult<()> {
    let length = password.chars().count();
    if length < MIN_PASSWORD {
        return Err(ApiError::BadRequest(format!(
            "Passwords need at least {MIN_PASSWORD} characters"
        )));
    }
    if length > MAX_PASSWORD {
        return Err(ApiError::BadRequest(format!(
            "Passwords are at most {MAX_PASSWORD} characters"
        )));
    }
    Ok(())
}

/// A signed-in session, as the cache keeps it.
#[derive(Debug, Clone, Copy)]
struct Session {
    user: UserId,
    expires_at: i64,
}

/// The signed-in account of a request, put there by [`middleware`].
#[derive(Debug, Clone, Copy)]
pub struct Viewer {
    pub user: UserId,
    token_hash: [u8; 32],
}

impl Viewer {
    pub const fn token_hash(&self) -> &[u8; 32] {
        &self.token_hash
    }

    /// A session of `user`, for tests.
    #[cfg(test)]
    pub fn test(user: UserId) -> Self {
        Self {
            user,
            token_hash: sha256(user.to_string().as_bytes()),
        }
    }
}

/// Attempts per key in a fixed window.
struct Limiter {
    limit: u32,
    window_ms: i64,
    counts: Mutex<HashMap<String, (i64, u32)>>,
}

/// Keys a limiter tracks at most. Past this, finished windows go first, then the oldest
/// windows, never all keys at once (that would reset an account under attack).
const MAX_LIMITER_KEYS: usize = 50_000;

impl Limiter {
    fn new(limit: u32, window_ms: i64) -> Self {
        Self {
            limit,
            window_ms,
            counts: Mutex::new(HashMap::new()),
        }
    }

    /// Whether `key` is under its limit; counts this attempt when it is.
    fn allow(&self, key: &str, now: i64) -> bool {
        let mut counts = self.counts.lock();
        if counts.len() >= MAX_LIMITER_KEYS {
            counts.retain(|_, (start, _)| now - *start < self.window_ms);
            if counts.len() >= MAX_LIMITER_KEYS {
                // Keep the newer half: the blocked keys of a current attack are recent.
                let mut starts: Vec<i64> = counts.values().map(|(start, _)| *start).collect();
                let middle = starts.len() / 2;
                let (_, cut, _) = starts.select_nth_unstable(middle);
                let cut = *cut;
                counts.retain(|_, (start, _)| *start >= cut);
            }
        }
        let (start, count) = counts.entry(key.to_owned()).or_insert((now, 0));
        if now - *start >= self.window_ms {
            *start = now;
            *count = 0;
        }
        if *count >= self.limit {
            return false;
        }
        *count += 1;
        true
    }

    /// Whether `key` is at its limit, without counting.
    fn blocked(&self, key: &str, now: i64) -> bool {
        self.counts
            .lock()
            .get(key)
            .is_some_and(|(start, count)| now - start < self.window_ms && *count >= self.limit)
    }

    fn forget(&self, key: &str) {
        self.counts.lock().remove(key);
    }
}

const MINUTE_MS: i64 = 60 * 1000;

/// The address a request came from: its IPv4 address, or its IPv6 /56 network (what ISPs
/// commonly give one customer), so one machine cannot rotate addresses past the limits.
fn client_key(parts: &Parts) -> String {
    let Some(ConnectInfo(address)) = parts.extensions.get::<ConnectInfo<SocketAddr>>() else {
        return "unknown".to_owned();
    };
    match address.ip().to_canonical() {
        IpAddr::V4(ip) => ip.to_string(),
        IpAddr::V6(ip) => {
            let s = ip.segments();
            format!("{:x}:{:x}:{:x}:{:x}::/56", s[0], s[1], s[2], s[3] & 0xff00)
        }
    }
}

/// The address a request came from, for the limits.
pub struct ClientAddress(pub String);

impl<S: Send + Sync> FromRequestParts<S> for ClientAddress {
    type Rejection = std::convert::Infallible;

    async fn from_request_parts(parts: &mut Parts, _: &S) -> Result<Self, Self::Rejection> {
        Ok(Self(client_key(parts)))
    }
}

/// The session cookie's name and attributes.
#[derive(Clone, Copy)]
pub struct Cookie {
    secure: bool,
}

impl Cookie {
    const fn name(self) -> &'static str {
        // `__Host-` makes browsers refuse the cookie unless it is Secure, for this host only
        // and for every path.
        if self.secure {
            "__Host-openleet-session"
        } else {
            "openleet-session"
        }
    }

    fn header(self, value: &str, max_age_ms: i64) -> HeaderValue {
        let secure = if self.secure { "; Secure" } else { "" };
        let max_age = max_age_ms.max(0) / 1000;
        HeaderValue::from_str(&format!(
            "{}={value}; Path=/; Max-Age={max_age}; HttpOnly; SameSite=Lax{secure}",
            self.name()
        ))
        .expect("cookie values are base64url")
    }

    /// Sets the session cookie to `token`.
    pub fn set(self, token: &str) -> HeaderValue {
        self.header(token, SESSION_MS)
    }

    /// Removes the session cookie.
    pub fn clear(self) -> HeaderValue {
        self.header("", 0)
    }

    /// The session token from the request's cookies, with its hash, if it holds a
    /// well-formed one.
    fn token(self, headers: &HeaderMap) -> Option<(&str, [u8; 32])> {
        let prefix = format!("{}=", self.name());
        headers
            .get_all(header::COOKIE)
            .iter()
            .filter_map(|value| value.to_str().ok())
            .flat_map(|value| value.split(';'))
            .filter_map(|pair| pair.trim().strip_prefix(&prefix))
            .find_map(|token| {
                let bytes = URL_SAFE_NO_PAD.decode(token).ok()?;
                (bytes.len() == 32).then(|| (token, sha256(&bytes)))
            })
    }
}

/// The one-time code that makes the first admin.
struct SetupCode {
    code: String,
    file: PathBuf,
}

/// Formats 16 random bytes as eight groups of four hex digits.
fn new_setup_code() -> String {
    let hex: String = random::<16>().iter().map(|b| format!("{b:02x}")).collect();
    hex.as_bytes()
        .chunks(4)
        .map(|c| std::str::from_utf8(c).expect("hex is ASCII"))
        .collect::<Vec<_>>()
        .join("-")
}

/// A typed setup code without spaces or dashes, lowercased.
fn plain_code(code: &str) -> String {
    code.chars()
        .filter(char::is_ascii_alphanumeric)
        .map(|c| c.to_ascii_lowercase())
        .collect()
}

fn write_private(path: &Path, text: &str) -> Result<()> {
    use std::io::Write as _;
    let mut options = std::fs::OpenOptions::new();
    options.write(true).create(true).truncate(true);
    #[cfg(unix)]
    std::os::unix::fs::OpenOptionsExt::mode(&mut options, 0o600);
    let mut file = options
        .open(path)
        .with_context(|| format!("writing {}", path.display()))?;
    file.write_all(text.as_bytes())?;
    Ok(())
}

/// What sign-in and sign-up need, shared by the handlers.
pub struct Auth {
    pub cookie: Cookie,
    sessions: RwLock<HashMap<[u8; 32], Session>>,
    users: RwLock<HashMap<UserId, User>>,
    signups_open: AtomicBool,
    setup: Mutex<Option<SetupCode>>,
    hashing: tokio::sync::Semaphore,
    /// Requests waiting for `hashing`.
    hashing_queue: AtomicUsize,
    /// Orders session writes with their cache updates, so two sign-ins of one account do not
    /// drop each other's session from the cache.
    session_writes: Mutex<()>,
    /// Accounts deleted since the start: no session, progress or write reaches them again.
    deleted: RwLock<HashSet<UserId>>,
    /// Verified when an email has no account, so a wrong email takes as long as a wrong
    /// password. Made on first use.
    decoy_hash: std::sync::OnceLock<String>,
    /// Every sign-in and sign-up attempt, per address.
    attempts: Limiter,
    /// Wrong passwords, per account and address (so nobody can lock an account out from
    /// elsewhere), and per signed-in account for its own password checks.
    failures: Limiter,
    /// Accounts made, per address.
    signups: Limiter,
}

/// What a session cookie leads to: the user, or why there is none.
pub struct NewSession {
    pub token: String,
    pub user: User,
}

impl Auth {
    /// Loads the accounts, live sessions and settings. Without a first admin, writes a new
    /// setup code to `state_dir`.
    pub fn load(store: &Store, state_dir: &Path, secure: bool, now: i64) -> Result<Self> {
        let users = store
            .users()?
            .into_iter()
            .map(|user| (user.id, user))
            .collect();
        let sessions = store
            .sessions(now)?
            .into_iter()
            .map(|s| {
                (
                    s.token_hash,
                    Session {
                        user: s.user,
                        expires_at: s.expires_at,
                    },
                )
            })
            .collect();
        let setup = if store.has_first_admin()? {
            let _ = std::fs::remove_file(state_dir.join(SETUP_FILE));
            None
        } else {
            let file = state_dir.join(SETUP_FILE);
            let code = new_setup_code();
            write_private(&file, &format!("{code}\n"))?;
            tracing::warn!(
                "no admin account yet: sign up with the setup code in {} to become the admin",
                file.display()
            );
            Some(SetupCode { code, file })
        };
        Ok(Self {
            cookie: Cookie { secure },
            sessions: RwLock::new(sessions),
            users: RwLock::new(users),
            signups_open: AtomicBool::new(store.signups_open()?),
            setup: Mutex::new(setup),
            hashing: tokio::sync::Semaphore::new(HASHING_AT_ONCE),
            hashing_queue: AtomicUsize::new(0),
            session_writes: Mutex::new(()),
            deleted: RwLock::new(HashSet::new()),
            decoy_hash: std::sync::OnceLock::new(),
            attempts: Limiter::new(30, 15 * MINUTE_MS),
            failures: Limiter::new(10, 15 * MINUTE_MS),
            signups: Limiter::new(10, 60 * MINUTE_MS),
        })
    }

    /// Whether the account was deleted.
    pub fn is_deleted(&self, id: UserId) -> bool {
        self.deleted.read().contains(&id)
    }

    /// The account, as cached.
    pub fn user(&self, id: UserId) -> Option<User> {
        self.users.read().get(&id).cloned()
    }

    pub fn user_count(&self) -> usize {
        self.users.read().len()
    }

    pub fn signups_open(&self) -> bool {
        self.signups_open.load(Ordering::Relaxed)
    }

    pub fn set_signups_open(&self, open: bool) {
        self.signups_open.store(open, Ordering::Relaxed);
    }

    /// Whether the first admin is still to be made with the setup code.
    pub fn needs_setup(&self) -> bool {
        self.setup.lock().is_some()
    }

    /// Whether `code` is the setup code (in constant time).
    pub fn setup_code_matches(&self, code: &str) -> bool {
        self.setup.lock().as_ref().is_some_and(|setup| {
            let (typed, expected) = (plain_code(code), plain_code(&setup.code));
            typed.len() == expected.len() && bool::from(typed.as_bytes().ct_eq(expected.as_bytes()))
        })
    }

    /// The first admin exists: the setup code is spent.
    pub fn finish_setup(&self) {
        if let Some(setup) = self.setup.lock().take()
            && let Err(error) = std::fs::remove_file(&setup.file)
        {
            tracing::warn!("could not remove {}: {error}", setup.file.display());
        }
    }

    /// Counts a sign-in or sign-up attempt from `address`.
    pub fn allow_attempt(&self, address: &str) -> ApiResult<()> {
        if self.attempts.allow(address, now_ms()) {
            Ok(())
        } else {
            Err(ApiError::TooMany(
                "Too many attempts from your network; try again in 15 minutes".into(),
            ))
        }
    }

    /// Refuses a password check with too many recent failures under `key` (see
    /// [`Auth::failures`]).
    pub fn check_failures(&self, key: &str) -> ApiResult<()> {
        if self.failures.blocked(key, now_ms()) {
            Err(ApiError::TooMany(
                "Too many wrong passwords for this account; try again in 15 minutes".into(),
            ))
        } else {
            Ok(())
        }
    }

    pub fn count_failure(&self, key: &str) {
        self.failures.allow(key, now_ms());
    }

    pub fn forget_failures(&self, key: &str) {
        self.failures.forget(key);
    }

    /// Counts an account made from `address`.
    pub fn allow_signup(&self, address: &str) -> ApiResult<()> {
        if self.signups.allow(address, now_ms()) {
            Ok(())
        } else {
            Err(ApiError::TooMany(
                "Too many new accounts from your network; try again in an hour".into(),
            ))
        }
    }

    /// Runs password hashing off the async workers, a few at a time. Past [`HASHING_QUEUE`]
    /// waiting requests, or [`HASHING_WAIT`], the request is refused.
    pub async fn hashing<T: Send + 'static>(
        &self,
        work: impl FnOnce() -> T + Send + 'static,
    ) -> ApiResult<T> {
        let busy = || ApiError::TooMany("The server is busy; try again in a moment".into());
        if self.hashing_queue.fetch_add(1, Ordering::AcqRel) >= HASHING_QUEUE {
            self.hashing_queue.fetch_sub(1, Ordering::AcqRel);
            return Err(busy());
        }
        let permit = tokio::time::timeout(HASHING_WAIT, self.hashing.acquire()).await;
        self.hashing_queue.fetch_sub(1, Ordering::AcqRel);
        let _permit = permit
            .map_err(|_| busy())?
            .map_err(|e| ApiError::Internal(e.into()))?;
        tokio::task::spawn_blocking(work)
            .await
            .map_err(|e| ApiError::Internal(e.into()))
    }

    /// The hash to verify against when an email has no account (call it off the async
    /// workers: the first call hashes).
    pub fn decoy_hash(&self) -> String {
        self.decoy_hash
            .get_or_init(|| {
                hash_password(&URL_SAFE_NO_PAD.encode(random::<16>()))
                    .expect("hashing a random password")
            })
            .clone()
    }

    /// Forgets a deleted account and every session of it, for good.
    pub fn forget_user(&self, id: UserId) {
        let _writes = self.session_writes.lock();
        self.deleted.write().insert(id);
        self.users.write().remove(&id);
        self.sessions.write().retain(|_, s| s.user != id);
    }

    /// Starts a session for `user`: stores it, ends the oldest beyond [`MAX_SESSIONS`], and
    /// returns the token for the cookie.
    pub fn start_session(&self, store: &Store, user: User, now: i64) -> Result<NewSession> {
        let _writes = self.session_writes.lock();
        anyhow::ensure!(!self.is_deleted(user.id), "{} was deleted", user.id);
        let token = random::<32>();
        let stored = StoredSession {
            token_hash: sha256(&token),
            user: user.id,
            expires_at: now + SESSION_MS,
        };
        let kept = store.insert_session(&stored, now, MAX_SESSIONS)?;
        let mut sessions = self.sessions.write();
        sessions.retain(|hash, s| s.user != user.id || kept.contains(hash));
        sessions.insert(
            stored.token_hash,
            Session {
                user: user.id,
                expires_at: stored.expires_at,
            },
        );
        drop(sessions);
        self.users.write().insert(user.id, user.clone());
        Ok(NewSession {
            token: URL_SAFE_NO_PAD.encode(token),
            user,
        })
    }

    /// Ends one session.
    pub fn end_session(&self, store: &Store, token_hash: &[u8; 32]) -> Result<()> {
        store.delete_session(token_hash)?;
        self.sessions.write().remove(token_hash);
        Ok(())
    }

    /// Ends every session of `user` but `keep` (after a password change).
    pub fn end_other_sessions(&self, user: UserId, keep: &[u8; 32]) {
        let _writes = self.session_writes.lock();
        self.sessions
            .write()
            .retain(|hash, s| s.user != user || hash == keep);
    }

    /// Drops expired sessions from the cache (the database drops them at the next start).
    pub fn prune(&self, now: i64) {
        self.sessions.write().retain(|_, s| s.expires_at > now);
    }

    /// The live session a request's cookie names, and, when `renew` and the session is due to
    /// be moved on, its cookie again.
    fn session(
        &self,
        headers: &HeaderMap,
        now: i64,
        renew: bool,
    ) -> Option<(Viewer, Option<Renewal>)> {
        let (token, token_hash) = self.cookie.token(headers)?;
        let session = *self.sessions.read().get(&token_hash)?;
        if session.expires_at <= now {
            self.sessions.write().remove(&token_hash);
            return None;
        }
        let due = session.expires_at - now < SESSION_MS - RENEW_AFTER_MS;
        let renew = (renew && due).then(|| {
            let expires_at = now + SESSION_MS;
            if let Some(cached) = self.sessions.write().get_mut(&token_hash) {
                cached.expires_at = expires_at;
            }
            Renewal {
                expires_at,
                cookie: self.cookie.set(token),
            }
        });
        Some((
            Viewer {
                user: session.user,
                token_hash,
            },
            renew,
        ))
    }
}

/// The one endpoint whose answer moves a session on.
const RENEWS_AT: &str = "/api/session";

/// A session moved on: its new end, and the cookie that tells the browser.
struct Renewal {
    expires_at: i64,
    cookie: HeaderValue,
}

/// Whether an unsafe request comes from another site. Browsers send `Sec-Fetch-Site`, which
/// pages cannot set, so it decides when present (a dev proxy may rewrite `Host`, never it).
/// Older browsers send only `Origin`, checked against `Host`. Clients with neither (curl, CI)
/// carry no ambient cookies of a victim's.
fn cross_site(headers: &HeaderMap) -> bool {
    let fetch_site = headers.get("sec-fetch-site").and_then(|v| v.to_str().ok());
    match fetch_site {
        Some("same-origin" | "none") => return false,
        Some(_) => return true,
        None => {}
    }
    let Some(origin) = headers.get(header::ORIGIN).and_then(|v| v.to_str().ok()) else {
        return false;
    };
    let host = headers.get(header::HOST).and_then(|v| v.to_str().ok());
    let origin_host = origin
        .strip_prefix("https://")
        .or_else(|| origin.strip_prefix("http://"));
    match (origin_host, host) {
        (Some(origin_host), Some(host)) => !origin_host.eq_ignore_ascii_case(host),
        _ => true,
    }
}

/// Names the signed-in account on each request ([`Viewer`] in its extensions), moves a
/// session on after a day of use, and refuses writes to the API from other sites.
///
/// Sessions move on only at `GET /api/session`, which every page load of the app asks for
/// first: its answer is private, so the renewed cookie never lands in a shared cache.
pub async fn middleware(State(state): State<Shared>, mut request: Request, next: Next) -> Response {
    let unsafe_method = !matches!(
        *request.method(),
        Method::GET | Method::HEAD | Method::OPTIONS
    );
    if unsafe_method && request.uri().path().starts_with("/api/") && cross_site(request.headers()) {
        return ApiError::Forbidden("Requests from other sites are not allowed".into())
            .into_response();
    }
    let now = now_ms();
    let renew = request.method() == Method::GET && request.uri().path() == RENEWS_AT;
    let session = state.auth.session(request.headers(), now, renew);
    let mut renewed = None;
    if let Some((viewer, renew)) = session {
        request.extensions_mut().insert(viewer);
        if let Some(Renewal { expires_at, cookie }) = renew {
            renewed = Some(cookie);
            let token_hash = viewer.token_hash;
            let state = Arc::clone(&state);
            tokio::spawn(async move {
                if let Err(error) = state
                    .db(move |store| store.extend_session(&token_hash, expires_at))
                    .await
                {
                    tracing::error!("could not extend a session: {error}");
                }
            });
        }
    }
    let mut response = next.run(request).await;
    // The same token with a fresh Max-Age, unless the handler set or cleared the cookie.
    if let Some(cookie) = renewed
        && !response.headers().contains_key(header::SET_COOKIE)
    {
        response.headers_mut().insert(header::SET_COOKIE, cookie);
    }
    response
}

/// The signed-in account and its progress, for handlers that read or write progress.
/// Without a session the request fails with 401 before the handler runs.
pub struct Me {
    pub user: UserId,
    pub learner: Arc<Learner>,
    pub viewer: Viewer,
}

impl FromRequestParts<Shared> for Me {
    type Rejection = ApiError;

    async fn from_request_parts(parts: &mut Parts, state: &Shared) -> ApiResult<Self> {
        let viewer = *parts.extensions.get::<Viewer>().ok_or(ApiError::SignIn)?;
        if state.auth.user(viewer.user).is_none() {
            return Err(ApiError::SignIn);
        }
        let learner = state.learner(viewer.user).await?;
        Ok(Self {
            user: viewer.user,
            learner,
            viewer,
        })
    }
}

#[cfg(test)]
impl Me {
    /// `user`, signed in, for handler tests.
    pub async fn test(state: &Shared, user: UserId) -> Self {
        Self {
            user,
            learner: state.learner(user).await.expect("load the account"),
            viewer: Viewer::test(user),
        }
    }
}

/// A signed-in admin; others get 403.
pub struct Admin(pub Viewer);

impl FromRequestParts<Shared> for Admin {
    type Rejection = ApiError;

    async fn from_request_parts(parts: &mut Parts, state: &Shared) -> ApiResult<Self> {
        let viewer = *parts.extensions.get::<Viewer>().ok_or(ApiError::SignIn)?;
        match state.auth.user(viewer.user) {
            Some(user) if user.admin => Ok(Self(viewer)),
            _ => Err(ApiError::Forbidden("Only an admin can do that".into())),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn hashes_are_argon2id_salted_and_verify() {
        let first = hash_password("correct horse").unwrap();
        let second = hash_password("correct horse").unwrap();
        assert!(
            first.starts_with("$argon2id$v=19$m=19456,t=2,p=1$"),
            "{first}"
        );
        assert_ne!(first, second, "each hash has its own salt");
        assert!(verify_password("correct horse", &first));
        assert!(!verify_password("correct horsf", &first));
        assert!(!verify_password("correct horse", "not a hash"));
    }

    #[test]
    fn emails_are_trimmed_lowercased_and_checked() {
        assert_eq!(
            normalize_email("  Ada@Example.COM ").as_deref(),
            Some("ada@example.com")
        );
        for bad in [
            "",
            "ada",
            "@example.com",
            "ada@",
            "ada@example",
            "ada@.com",
            "a da@example.com",
            "ada@exam\nple.com",
            "<ada@example.com>",
        ] {
            assert_eq!(normalize_email(bad), None, "{bad:?}");
        }
        assert_eq!(
            normalize_email(&format!("{}@example.com", "a".repeat(250))),
            None
        );
    }

    #[test]
    fn passwords_need_8_to_128_characters() {
        assert!(check_password("1234567").is_err());
        assert!(check_password("12345678").is_ok());
        assert!(check_password(&"é".repeat(128)).is_ok());
        assert!(check_password(&"a".repeat(129)).is_err());
    }

    #[test]
    fn limiters_count_per_key_in_windows() {
        let limiter = Limiter::new(2, 1000);
        assert!(limiter.allow("a", 0) && limiter.allow("a", 1));
        assert!(!limiter.allow("a", 2) && limiter.blocked("a", 2));
        assert!(limiter.allow("b", 2), "other keys are not limited");
        assert!(!limiter.blocked("a", 1000) && limiter.allow("a", 1000));
        limiter.forget("a");
        assert!(!limiter.blocked("a", 1001));
    }

    #[test]
    fn sessions_move_on_after_a_day_only_where_asked() {
        let dir = crate::db::testing::TempDir::new("auth-renew");
        let (store, _) = Store::open(&dir.path("o.duckdb"), &dir.path("none")).unwrap();
        let auth = Auth::load(&store, dir.root(), true, 0).unwrap();
        let user = User {
            id: UserId::test(7),
            email: "a@example.com".into(),
            admin: false,
        };
        let session = auth.start_session(&store, user, 0).unwrap();
        let mut headers = HeaderMap::new();
        headers.insert(
            header::COOKIE,
            HeaderValue::from_str(&format!("__Host-openleet-session={}", session.token)).unwrap(),
        );
        let renewed = |now, renew| auth.session(&headers, now, renew).map(|(_, r)| r.is_some());
        assert_eq!(renewed(DAY_MS / 2, true), Some(false), "not yet due");
        assert_eq!(renewed(2 * DAY_MS, false), Some(false), "not asked");
        assert_eq!(renewed(2 * DAY_MS, true), Some(true));
        // Moved on: alive 30 days after its last renewal, not after sign-in.
        assert_eq!(renewed(2 * DAY_MS + SESSION_MS - 1, false), Some(false));
        assert_eq!(renewed(2 * DAY_MS + SESSION_MS, false), None, "ended");
    }

    #[test]
    fn a_full_limiter_drops_the_oldest_windows_not_every_key() {
        let limiter = Limiter::new(1, 1_000_000);
        assert!(limiter.allow("target", MAX_LIMITER_KEYS as i64));
        assert!(limiter.blocked("target", MAX_LIMITER_KEYS as i64));
        // A flood of other keys, older than the target's window, fills the limiter.
        for i in 1..MAX_LIMITER_KEYS {
            limiter.allow(&format!("old {i}"), i64::try_from(i).unwrap() % 1000);
        }
        limiter.allow("one more", MAX_LIMITER_KEYS as i64 + 1);
        assert!(limiter.blocked("target", MAX_LIMITER_KEYS as i64 + 2));
        assert!(limiter.counts.lock().len() <= MAX_LIMITER_KEYS / 2 + 2);
    }

    #[test]
    fn setup_codes_ignore_case_and_dashes() {
        let code = new_setup_code();
        assert_eq!(code.len(), 39);
        assert_eq!(plain_code(&code).len(), 32);
        assert_eq!(plain_code(" ABCD-ef01 "), "abcdef01");
    }

    #[test]
    fn cookies_are_http_only_lax_and_secure_over_https() {
        let secure = Cookie { secure: true }.set("tok");
        assert_eq!(
            secure,
            "__Host-openleet-session=tok; Path=/; Max-Age=2592000; HttpOnly; SameSite=Lax; Secure"
        );
        let plain = Cookie { secure: false }.clear();
        assert_eq!(
            plain,
            "openleet-session=; Path=/; Max-Age=0; HttpOnly; SameSite=Lax"
        );
        let token = [7_u8; 32];
        let mut headers = HeaderMap::new();
        headers.insert(
            header::COOKIE,
            HeaderValue::from_str(&format!(
                "theme=dark; openleet-session={}",
                URL_SAFE_NO_PAD.encode(token)
            ))
            .unwrap(),
        );
        assert_eq!(
            Cookie { secure: false }.token(&headers).map(|t| t.1),
            Some(sha256(&token))
        );
        // The other name, a short token or junk is no session.
        assert_eq!(Cookie { secure: true }.token(&headers), None);
        headers.insert(
            header::COOKIE,
            HeaderValue::from_static("openleet-session=abc"),
        );
        assert_eq!(Cookie { secure: false }.token(&headers), None);
    }

    #[test]
    fn writes_from_other_sites_are_cross_site() {
        let headers = |pairs: &[(&str, &str)]| {
            let mut map = HeaderMap::new();
            for (name, value) in pairs {
                map.insert(
                    axum::http::HeaderName::from_bytes(name.as_bytes()).unwrap(),
                    HeaderValue::from_str(value).unwrap(),
                );
            }
            map
        };
        assert!(!cross_site(&headers(&[])));
        assert!(!cross_site(&headers(&[
            ("host", "openleet.example"),
            ("origin", "https://openleet.example"),
            ("sec-fetch-site", "same-origin"),
        ])));
        assert!(cross_site(&headers(&[
            ("host", "openleet.example"),
            ("origin", "https://evil.example"),
        ])));
        assert!(cross_site(&headers(&[("sec-fetch-site", "cross-site")])));
        assert!(cross_site(&headers(&[("sec-fetch-site", "same-site")])));
        assert!(cross_site(&headers(&[
            ("host", "openleet.example"),
            ("origin", "null"),
        ])));
        // Behind a dev proxy that rewrites Host, the browser's own word decides.
        assert!(!cross_site(&headers(&[
            ("host", "127.0.0.1:8080"),
            ("origin", "http://localhost:3000"),
            ("sec-fetch-site", "same-origin"),
        ])));
    }
}
