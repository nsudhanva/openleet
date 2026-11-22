//! Accounts: sign up, sign in and out, the signed-in account, its password and its deletion,
//! and the admin's settings. See `crate::auth` for how sessions and passwords work.

use axum::Json;
use axum::extract::{Query, State};
use axum::http::{StatusCode, header};
use axum::response::{IntoResponse, Response};
use serde::{Deserialize, Serialize};

use crate::auth::{
    self, Admin, ClientAddress, MAX_USERS, Me, NewSession, Viewer, check_password, normalize_email,
};
use openleet::readiness::Readiness;

use super::{Params, param};
use crate::db::{NewUser, User};
use crate::error::{ApiError, ApiResult};
use crate::state::{Shared, now_ms};

/// An account as the API shows it.
#[derive(Serialize)]
struct Account<'a> {
    email: &'a str,
    admin: bool,
}

impl<'a> From<&'a User> for Account<'a> {
    fn from(user: &'a User) -> Self {
        Self {
            email: &user.email,
            admin: user.admin,
        }
    }
}

/// `GET /api/session`.
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct SessionView<'a> {
    /// The signed-in account; `null` when signed out.
    user: Option<Account<'a>>,
    /// The account's readiness for `?company=` (the header's figure); `null` when signed out.
    readiness: Option<&'a Readiness>,
    signups_open: bool,
    /// Whether the first admin is still to sign up with the setup code.
    needs_setup: bool,
}

/// `?company=`: who is signed in, their readiness for the company, and whether sign-up is
/// open. Never a 401: every page asks first, signed in or not.
pub async fn session(
    State(state): State<Shared>,
    viewer: Option<axum::Extension<Viewer>>,
    Query(params): Params,
) -> ApiResult<Response> {
    let user = viewer.and_then(|v| state.auth.user(v.user));
    let report = match &user {
        Some(user) => {
            let company = state.content.company_or_default(param(&params, "company"));
            let learner = state.learner(user.id).await?;
            let (_, report) = learner.report(&state.content, company, now_ms());
            Some(report)
        }
        None => None,
    };
    Ok(Json(&SessionView {
        user: user.as_ref().map(Account::from),
        readiness: report.as_deref().map(|r| &r.readiness),
        signups_open: state.auth.signups_open(),
        needs_setup: state.auth.needs_setup(),
    })
    .into_response())
}

/// Body of sign-in and sign-up.
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Credentials {
    email: String,
    password: String,
    /// Sign-up only: the server's setup code, to make the first admin.
    #[serde(default)]
    setup_code: Option<String>,
}

/// A response that signs the browser in.
fn signed_in(state: &Shared, status: StatusCode, session: &NewSession) -> Response {
    (
        status,
        [(header::SET_COOKIE, state.auth.cookie.set(&session.token))],
        Json(&Account::from(&session.user)),
    )
        .into_response()
}

/// Starts a session for a user that just signed up or in.
async fn start_session(state: &Shared, user: User) -> ApiResult<NewSession> {
    let shared = std::sync::Arc::clone(state);
    state
        .db(move |store| shared.auth.start_session(store, user, now_ms()))
        .await
}

/// `POST /api/session`: signs in with an email and password. A wrong email and a wrong
/// password get the same answer, after the same work.
pub async fn sign_in(
    State(state): State<Shared>,
    ClientAddress(address): ClientAddress,
    previous: Option<axum::Extension<Viewer>>,
    Json(input): Json<Credentials>,
) -> ApiResult<Response> {
    state.auth.allow_attempt(&address)?;
    let email = normalize_email(&input.email).unwrap_or_default();
    // Per account and address: others cannot lock the account out by guessing wrong.
    let failures = format!("{email} from {address}");
    state.auth.check_failures(&failures)?;
    let lookup = email.clone();
    let found = state.db(move |store| store.credentials(&lookup)).await?;
    let shared = std::sync::Arc::clone(&state);
    let password = input.password;
    let user = state
        .auth
        .hashing(move || match found {
            Some(found) if auth::verify_password(&password, &found.password_hash) => {
                Some(found.user)
            }
            Some(_) => None,
            None => {
                auth::verify_password(&password, &shared.auth.decoy_hash());
                None
            }
        })
        .await?;
    let Some(user) = user.filter(|u| !state.auth.is_deleted(u.id)) else {
        state.auth.count_failure(&failures);
        return Err(ApiError::WrongCredentials);
    };
    state.auth.forget_failures(&failures);
    tracing::info!("{} signed in", user.id);
    end_previous(&state, previous).await?;
    let session = start_session(&state, user).await?;
    Ok(signed_in(&state, StatusCode::OK, &session))
}

/// Ends the browser's session, if it has one (signing in again replaces it).
async fn end_previous(state: &Shared, viewer: Option<axum::Extension<Viewer>>) -> ApiResult<()> {
    if let Some(axum::Extension(viewer)) = viewer {
        let shared = std::sync::Arc::clone(state);
        let hash = *viewer.token_hash();
        state
            .db(move |store| shared.auth.end_session(store, &hash))
            .await?;
    }
    Ok(())
}

/// `DELETE /api/session`: signs out this browser.
pub async fn sign_out(
    State(state): State<Shared>,
    viewer: Option<axum::Extension<Viewer>>,
) -> ApiResult<Response> {
    end_previous(&state, viewer).await?;
    Ok((
        StatusCode::NO_CONTENT,
        [(header::SET_COOKIE, state.auth.cookie.clear())],
    )
        .into_response())
}

/// `POST /api/users`: makes an account and signs it in. With the setup code it makes the
/// first admin, who owns the progress from before accounts; otherwise sign-ups must be open.
pub async fn sign_up(
    State(state): State<Shared>,
    ClientAddress(address): ClientAddress,
    previous: Option<axum::Extension<Viewer>>,
    Json(input): Json<Credentials>,
) -> ApiResult<Response> {
    state.auth.allow_attempt(&address)?;
    let email = normalize_email(&input.email)
        .ok_or_else(|| ApiError::BadRequest("Enter an email address".into()))?;
    check_password(&input.password)?;
    let first_admin = match input.setup_code.as_deref().map(str::trim) {
        Some(code) if !code.is_empty() => {
            if !state.auth.setup_code_matches(code) {
                return Err(ApiError::Forbidden("That setup code is not right".into()));
            }
            true
        }
        _ => {
            if state.auth.needs_setup() {
                return Err(ApiError::Forbidden(
                    "Sign-up opens once the admin account exists".into(),
                ));
            }
            if !state.auth.signups_open() {
                return Err(ApiError::Forbidden("Sign-ups are closed".into()));
            }
            if state.auth.user_count() >= MAX_USERS {
                return Err(ApiError::Forbidden(
                    "This server takes no more accounts".into(),
                ));
            }
            false
        }
    };
    state.auth.allow_signup(&address)?;
    let password = input.password;
    let hash = state
        .auth
        .hashing(move || auth::hash_password(&password))
        .await?
        .map_err(ApiError::Internal)?;
    let stored = email.clone();
    let created = state
        .db(move |store| store.create_user(&stored, &hash, first_admin, now_ms()))
        .await?;
    let id = match created {
        NewUser::Created(id) => id,
        NewUser::Taken => {
            return Err(ApiError::Conflict(
                "That email already has an account; sign in instead".into(),
            ));
        }
        NewUser::AdminExists => {
            return Err(ApiError::Forbidden("The admin account exists".into()));
        }
    };
    if first_admin {
        state.auth.finish_setup();
    }
    tracing::info!(
        "{id} signed up{}",
        if first_admin { " as the admin" } else { "" }
    );
    let user = User {
        id,
        email,
        admin: first_admin,
    };
    end_previous(&state, previous).await?;
    let session = start_session(&state, user).await?;
    Ok(signed_in(&state, StatusCode::CREATED, &session))
}

/// Body of `PUT /api/account/password`.
#[derive(Deserialize)]
pub struct PasswordChange {
    current: String,
    password: String,
}

/// Checks the account's current password, off the async workers. Wrong passwords count
/// against the account, so a borrowed session cannot guess its way to a takeover.
async fn check_current(state: &Shared, me: &Me, password: String) -> ApiResult<()> {
    let failures = format!("{} (signed in)", me.user);
    state.auth.check_failures(&failures)?;
    let user = me.user;
    let hash = state
        .db(move |store| store.password_hash(user))
        .await?
        .ok_or(ApiError::SignIn)?;
    let right = state
        .auth
        .hashing(move || auth::verify_password(&password, &hash))
        .await?;
    if right {
        state.auth.forget_failures(&failures);
        Ok(())
    } else {
        state.auth.count_failure(&failures);
        Err(ApiError::Forbidden(
            "Your current password is not right".into(),
        ))
    }
}

/// `PUT /api/account/password`: a new password, given the current one. Every other session
/// of the account ends; this one stays.
pub async fn change_password(
    State(state): State<Shared>,
    ClientAddress(address): ClientAddress,
    me: Me,
    Json(input): Json<PasswordChange>,
) -> ApiResult<StatusCode> {
    state.auth.allow_attempt(&address)?;
    check_password(&input.password)?;
    check_current(&state, &me, input.current).await?;
    let password = input.password;
    let hash = state
        .auth
        .hashing(move || auth::hash_password(&password))
        .await?
        .map_err(ApiError::Internal)?;
    let (user, keep) = (me.user, *me.viewer.token_hash());
    state
        .db(move |store| store.set_password(user, &hash, &keep, now_ms()))
        .await?;
    state.auth.end_other_sessions(user, &keep);
    tracing::info!("{user} changed their password");
    Ok(StatusCode::NO_CONTENT)
}

/// Body of `DELETE /api/account`.
#[derive(Deserialize)]
pub struct Deletion {
    password: String,
}

/// `DELETE /api/account`: deletes the account and all its progress, given its password.
/// The admin stays: someone must be able to change the settings.
pub async fn delete_account(
    State(state): State<Shared>,
    ClientAddress(address): ClientAddress,
    me: Me,
    Json(input): Json<Deletion>,
) -> ApiResult<Response> {
    state.auth.allow_attempt(&address)?;
    if state.auth.user(me.user).is_some_and(|u| u.admin) {
        return Err(ApiError::BadRequest(
            "The admin account cannot be deleted".into(),
        ));
    }
    check_current(&state, &me, input.password).await?;
    state.delete_account(&me.learner).await?;
    tracing::info!("{} deleted their account", me.user);
    Ok((
        StatusCode::NO_CONTENT,
        [(header::SET_COOKIE, state.auth.cookie.clear())],
    )
        .into_response())
}

/// `GET /api/admin/settings`.
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub struct Settings {
    signups_open: bool,
    users: usize,
}

fn settings_of(state: &Shared) -> Json<Settings> {
    Json(Settings {
        signups_open: state.auth.signups_open(),
        users: state.auth.user_count(),
    })
}

/// The server settings and the number of accounts; admins only.
pub async fn settings(State(state): State<Shared>, _: Admin) -> Json<Settings> {
    settings_of(&state)
}

/// Body of `PATCH /api/admin/settings`.
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct SettingsEdit {
    signups_open: Option<bool>,
}

/// Opens or closes sign-up; admins only.
pub async fn edit_settings(
    State(state): State<Shared>,
    Admin(admin): Admin,
    Json(edit): Json<SettingsEdit>,
) -> ApiResult<Json<Settings>> {
    if let Some(open) = edit.signups_open {
        state.db(move |store| store.set_signups_open(open)).await?;
        state.auth.set_signups_open(open);
        tracing::info!(
            "{} {} sign-ups",
            admin.user,
            if open { "opened" } else { "closed" }
        );
    }
    Ok(settings_of(&state))
}
