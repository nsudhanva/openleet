//! Accounts end to end, through the whole app as a browser reaches it: sign-up with the setup
//! code, sign-in, sessions and their cookies, the admin's settings, and that no account's
//! progress reaches another. Every endpoint that reads progress is compared between an
//! account that saw another account's activity and one that never did.

use std::path::Path;
use std::sync::Arc;

use axum::body::{Body, to_bytes};
use axum::http::{Method, Request, StatusCode, header};
use serde_json::{Value, json};
use tower::ServiceExt as _;

use crate::api;
use crate::db::testing::TempDir;
use crate::db::{NewSubmission, UserId};
use crate::state::Shared;

const PASSWORD: &str = "correct horse battery";

/// A browser: the app, its session cookie and its address.
#[derive(Clone)]
struct Browser {
    app: axum::Router,
    cookie: Option<String>,
    address: std::net::SocketAddr,
}

struct Reply {
    status: StatusCode,
    body: Value,
    set_cookie: Option<String>,
}

impl Browser {
    fn new(state: &Shared) -> Self {
        Self {
            app: crate::app(Arc::clone(state)),
            cookie: None,
            address: "203.0.113.1:50000".parse().expect("address"),
        }
    }

    async fn send(&mut self, method: Method, uri: &str, body: Option<Value>) -> Reply {
        let mut request = Request::builder()
            .method(method)
            .uri(uri)
            .header(header::HOST, "openleet.test");
        if let Some(cookie) = &self.cookie {
            request = request.header(header::COOKIE, cookie);
        }
        let mut request = match body {
            Some(body) => request
                .header(header::CONTENT_TYPE, "application/json")
                .body(Body::from(body.to_string())),
            None => request.body(Body::empty()),
        }
        .expect("request");
        request
            .extensions_mut()
            .insert(axum::extract::ConnectInfo(self.address));
        let response = self.app.clone().oneshot(request).await.expect("response");
        let status = response.status();
        let set_cookie = response
            .headers()
            .get(header::SET_COOKIE)
            .map(|v| v.to_str().expect("ASCII").to_owned());
        if let Some(set) = &set_cookie {
            let pair = set.split(';').next().expect("a pair");
            self.cookie = pair
                .split_once('=')
                .filter(|(_, value)| !value.is_empty())
                .map(|_| pair.to_owned());
        }
        let bytes = to_bytes(response.into_body(), 1 << 26).await.expect("body");
        let body = if bytes.is_empty() {
            Value::Null
        } else {
            serde_json::from_slice(&bytes).unwrap_or_else(|_| Value::String("<html>".into()))
        };
        Reply {
            status,
            body,
            set_cookie,
        }
    }

    async fn get(&mut self, uri: &str) -> Reply {
        self.send(Method::GET, uri, None).await
    }

    async fn ok(&mut self, method: Method, uri: &str, body: Option<Value>) -> Value {
        let reply = self.send(method.clone(), uri, body).await;
        assert!(
            reply.status.is_success(),
            "{method} {uri}: {} {}",
            reply.status,
            reply.body
        );
        reply.body
    }

    async fn sign_up(&mut self, email: &str, setup_code: Option<&str>) -> Reply {
        self.send(
            Method::POST,
            "/api/users",
            Some(json!({"email": email, "password": PASSWORD, "setupCode": setup_code})),
        )
        .await
    }

    async fn sign_in(&mut self, email: &str, password: &str) -> Reply {
        self.send(
            Method::POST,
            "/api/session",
            Some(json!({"email": email, "password": password})),
        )
        .await
    }
}

fn state(dir: &TempDir) -> Shared {
    api::testing::state(dir)
}

fn setup_code(dir: &Path) -> String {
    std::fs::read_to_string(dir.join("setup-code"))
        .expect("the setup code file")
        .trim()
        .to_owned()
}

/// The user id of the account with this email.
fn user_id(state: &Shared, email: &str) -> UserId {
    state
        .store
        .credentials(email)
        .expect("look up")
        .expect("an account")
        .user
        .id
}

/// Every read of progress, as status and body. Ids of the other account's plan, list and
/// submission are asked for too.
async fn snapshot(browser: &mut Browser, other: &Others) -> Vec<(String, StatusCode, Value)> {
    let list = other.list.to_string();
    let mut uris = vec![
        "/api/session?company=google".to_owned(),
        "/api/readiness".to_owned(),
        "/api/readiness?company=meta".to_owned(),
        "/api/deck".to_owned(),
        "/api/deck?set=all&slug=two-sum".to_owned(),
        "/api/deck?set=due".to_owned(),
        "/api/problems".to_owned(),
        "/api/problems?status=solved".to_owned(),
        "/api/problems?status=shaky".to_owned(),
        format!("/api/problems?list={list}"),
        "/api/problems/two-sum".to_owned(),
        "/api/report?company=google".to_owned(),
        "/api/report?company=any".to_owned(),
        "/api/next".to_owned(),
        "/api/next?slug=two-sum".to_owned(),
        format!("/api/next?list={list}"),
        format!("/api/next?list={list}&slug=two-sum"),
        "/api/plans".to_owned(),
        "/api/lists".to_owned(),
        "/api/code/two-sum".to_owned(),
        "/api/submissions?slug=two-sum".to_owned(),
        format!("/api/submissions/{}", other.submission),
    ];
    uris.push(format!("/api/submissions/{}", other.submission + 1));
    let mut seen = Vec::new();
    for uri in uris {
        let mut reply = browser.get(&uri).await;
        // Only who is signed in and when a report was computed differ.
        if let Some(user) = reply.body.get_mut("user") {
            *user = Value::Null;
        }
        if let Some(report) = reply.body.get_mut("report") {
            report["computedAt"] = Value::Null;
        }
        seen.push((uri, reply.status, reply.body));
    }
    seen
}

/// Ids of one account's rows that another may try to reach.
struct Others {
    plan: i64,
    list: i64,
    submission: i64,
}

/// Fills an account with every kind of progress, through the API where the API writes it
/// (a submission needs the judge, so it goes straight to the database and the account's
/// memory, as `POST /api/submit` would leave them).
async fn practice(state: &Shared, browser: &mut Browser, email: &str) -> Others {
    browser
        .ok(
            Method::POST,
            "/api/attempts",
            Some(json!({"slug": "two-sum", "grade": "good", "guessed": ["Array"], "hints": 1})),
        )
        .await;
    browser
        .ok(
            Method::POST,
            "/api/attempts",
            Some(json!({"slug": "add-two-numbers", "grade": "again", "guessed": ["Math"]})),
        )
        .await;
    browser
        .ok(
            Method::PUT,
            "/api/notes",
            Some(json!({"slug": "two-sum", "text": format!("{email}'s note")})),
        )
        .await;
    browser
        .ok(
            Method::PUT,
            "/api/drafts",
            Some(json!({"slug": "two-sum", "code": format!("# {email}")})),
        )
        .await;
    browser
        .ok(
            Method::POST,
            "/api/drafts/reset",
            Some(json!({"slug": "add-two-numbers", "code": format!("# {email} old")})),
        )
        .await;
    let plan = browser
        .ok(
            Method::PUT,
            "/api/plans",
            Some(json!({"company": "meta", "period": "3m", "status": "all"})),
        )
        .await["id"]
        .as_i64()
        .expect("plan id");
    browser
        .ok(
            Method::PATCH,
            &format!("/api/plans/{plan}"),
            Some(json!({"name": format!("{email} plan"), "pinned": true})),
        )
        .await;
    let list = browser
        .ok(
            Method::POST,
            "/api/lists",
            Some(
                json!({"name": format!("{email} list"), "slugs": ["basic-calculator", "two-sum"]}),
            ),
        )
        .await["id"]
        .as_i64()
        .expect("list id");
    let user = user_id(state, email);
    let learner = state.learner(user).await.expect("learner");
    let mut submission = 0;
    for verdict in [
        openleet_proto::Verdict::WrongAnswer,
        openleet_proto::Verdict::Accepted,
    ] {
        let name = verdict.as_str();
        submission = state
            .store
            .insert_submission(
                user,
                &NewSubmission {
                    slug: "two-sum",
                    at: crate::state::now_ms(),
                    code: &format!("# {email} solution"),
                    verdict: name,
                    passed: 1,
                    total: 2,
                    cpu_ms: 5,
                    detail: "null",
                },
            )
            .expect("submission");
        learner
            .progress
            .write()
            .record_submission("two-sum", crate::state::now_ms(), verdict);
    }
    Others {
        plan,
        list,
        submission,
    }
}

#[tokio::test]
async fn the_first_admin_needs_the_setup_code_and_then_others_sign_up() {
    let dir = TempDir::new("accounts-setup");
    let state = state(&dir);
    let mut admin = Browser::new(&state);
    let session = admin.get("/api/session").await.body;
    assert_eq!(
        session,
        json!({"user": null, "readiness": null, "signupsOpen": true, "needsSetup": true})
    );
    // Before the admin exists nobody else gets in, and a wrong code is refused.
    let mut early = Browser::new(&state);
    assert_eq!(
        early.sign_up("early@example.com", None).await.status,
        StatusCode::FORBIDDEN
    );
    assert_eq!(
        early
            .sign_up("early@example.com", Some("0000-0000"))
            .await
            .status,
        StatusCode::FORBIDDEN
    );
    let code = setup_code(dir.root());
    let made = admin
        .sign_up("  Admin@Example.com ", Some(&code.to_uppercase()))
        .await;
    assert_eq!(made.status, StatusCode::CREATED);
    assert_eq!(
        made.body,
        json!({"email": "admin@example.com", "admin": true})
    );
    let cookie = made.set_cookie.expect("a session cookie");
    assert!(
        cookie.starts_with("openleet-session=")
            && cookie.contains("HttpOnly")
            && cookie.contains("SameSite=Lax"),
        "{cookie}"
    );
    assert_eq!(user_id(&state, "admin@example.com"), UserId::FIRST_ADMIN);
    // The code is spent: its file is gone and it makes no second admin.
    assert!(!dir.path("setup-code").exists());
    let again = early.sign_up("second@example.com", Some(&code)).await;
    assert_eq!(again.status, StatusCode::FORBIDDEN);
    // Sign-up is open to anyone, as plain accounts; each email once, in any case.
    let member = early.sign_up("member@example.com", None).await;
    assert_eq!(member.status, StatusCode::CREATED);
    assert_eq!(member.body["admin"], false);
    let mut twin = Browser::new(&state);
    assert_eq!(
        twin.sign_up("MEMBER@example.com", None).await.status,
        StatusCode::CONFLICT
    );
    // Bad input.
    for (email, password) in [("not-an-email", PASSWORD), ("x@example.com", "short")] {
        let reply = twin
            .send(
                Method::POST,
                "/api/users",
                Some(json!({"email": email, "password": password})),
            )
            .await;
        assert_eq!(reply.status, StatusCode::BAD_REQUEST, "{email}");
    }

    // The admin closes sign-up; a member may not touch the settings.
    assert_eq!(
        early.get("/api/admin/settings").await.status,
        StatusCode::FORBIDDEN
    );
    assert_eq!(
        early
            .send(
                Method::PATCH,
                "/api/admin/settings",
                Some(json!({"signupsOpen": false}))
            )
            .await
            .status,
        StatusCode::FORBIDDEN
    );
    let closed = admin
        .ok(
            Method::PATCH,
            "/api/admin/settings",
            Some(json!({"signupsOpen": false})),
        )
        .await;
    assert_eq!(closed, json!({"signupsOpen": false, "users": 2}));
    assert_eq!(
        twin.sign_up("late@example.com", None).await.status,
        StatusCode::FORBIDDEN
    );
    assert_eq!(twin.get("/api/session").await.body["signupsOpen"], false);
    // It stays closed after a restart.
    assert!(!state.store.signups_open().unwrap());
    // Signing in still works.
    assert_eq!(
        twin.sign_in("member@example.com", PASSWORD).await.status,
        StatusCode::OK
    );
}

#[tokio::test]
async fn sign_in_out_and_password_changes_end_the_right_sessions() {
    let dir = TempDir::new("accounts-sessions");
    let state = state(&dir);
    let mut admin = Browser::new(&state);
    admin
        .sign_up("admin@example.com", Some(&setup_code(dir.root())))
        .await;
    let mut laptop = Browser::new(&state);
    assert_eq!(
        laptop.sign_up("ada@example.com", None).await.status,
        StatusCode::CREATED
    );
    let mut phone = Browser::new(&state);
    // A wrong password and an unknown email get the same answer.
    let wrong = phone.sign_in("ada@example.com", "wrong password").await;
    let unknown = phone.sign_in("nobody@example.com", PASSWORD).await;
    assert_eq!(wrong.status, StatusCode::UNAUTHORIZED);
    assert_eq!((unknown.status, &unknown.body), (wrong.status, &wrong.body));
    assert!(wrong.set_cookie.is_none() && phone.cookie.is_none());
    assert_eq!(
        phone.sign_in(" ADA@example.com", PASSWORD).await.status,
        StatusCode::OK
    );
    assert_eq!(
        phone.get("/api/session").await.body["user"]["email"],
        "ada@example.com"
    );

    // A forged or stolen-looking cookie is no session.
    let mut forged = Browser::new(&state);
    forged.cookie = Some(format!("openleet-session={}", "A".repeat(43)));
    assert_eq!(
        forged.get("/api/plans").await.status,
        StatusCode::UNAUTHORIZED
    );
    assert_eq!(forged.get("/api/session").await.body["user"], Value::Null);

    // A new password needs the current one, and ends the account's other sessions only.
    let refused = laptop
        .send(
            Method::PUT,
            "/api/account/password",
            Some(json!({"current": "wrong password", "password": "a new password"})),
        )
        .await;
    assert_eq!(refused.status, StatusCode::FORBIDDEN);
    laptop
        .ok(
            Method::PUT,
            "/api/account/password",
            Some(json!({"current": PASSWORD, "password": "a new password"})),
        )
        .await;
    assert_eq!(laptop.get("/api/plans").await.status, StatusCode::OK);
    assert_eq!(
        phone.get("/api/plans").await.status,
        StatusCode::UNAUTHORIZED
    );
    assert_eq!(admin.get("/api/plans").await.status, StatusCode::OK);
    assert_eq!(
        phone.sign_in("ada@example.com", PASSWORD).await.status,
        StatusCode::UNAUTHORIZED
    );
    assert_eq!(
        phone
            .sign_in("ada@example.com", "a new password")
            .await
            .status,
        StatusCode::OK
    );

    // Signing out ends this browser's session, server side too: the old cookie is dead.
    let old_cookie = laptop.cookie.clone();
    let out = laptop.send(Method::DELETE, "/api/session", None).await;
    assert_eq!(out.status, StatusCode::NO_CONTENT);
    assert!(out.set_cookie.unwrap().contains("Max-Age=0"));
    laptop.cookie = old_cookie;
    assert_eq!(
        laptop.get("/api/plans").await.status,
        StatusCode::UNAUTHORIZED
    );
    assert_eq!(phone.get("/api/plans").await.status, StatusCode::OK);

    // Sessions survive a restart: the database has them (hashed).
    let restarted = crate::auth::Auth::load(&state.store, dir.root(), false, 0).unwrap();
    assert_eq!(restarted.user_count(), 2);
    let stored = state.store.sessions(0).unwrap();
    assert_eq!(stored.len(), 2, "the admin's and the phone's");
    let token = phone
        .cookie
        .as_deref()
        .and_then(|c| c.split_once('='))
        .map(|(_, t)| t.to_owned())
        .unwrap();
    assert!(
        stored
            .iter()
            .all(|s| !s.token_hash.starts_with(token.as_bytes()))
    );
}

#[tokio::test]
async fn writes_from_other_sites_are_refused() {
    let dir = TempDir::new("accounts-csrf");
    let state = state(&dir);
    let mut admin = Browser::new(&state);
    admin
        .sign_up("admin@example.com", Some(&setup_code(dir.root())))
        .await;
    let request = |origin: &str, site: &str| {
        let mut request = Request::builder()
            .method(Method::PUT)
            .uri("/api/notes")
            .header(header::HOST, "openleet.test")
            .header(header::CONTENT_TYPE, "application/json")
            .header(header::COOKIE, admin.cookie.clone().unwrap());
        if !origin.is_empty() {
            request = request.header(header::ORIGIN, origin);
        }
        if !site.is_empty() {
            request = request.header("sec-fetch-site", site);
        }
        request
            .body(Body::from(r#"{"slug":"two-sum","text":"x"}"#))
            .unwrap()
    };
    for (origin, site, status) in [
        ("https://evil.example", "cross-site", StatusCode::FORBIDDEN),
        ("https://evil.example", "", StatusCode::FORBIDDEN),
        ("", "same-site", StatusCode::FORBIDDEN),
        ("http://openleet.test", "same-origin", StatusCode::OK),
    ] {
        let response = admin
            .app
            .clone()
            .oneshot(request(origin, site))
            .await
            .unwrap();
        assert_eq!(response.status(), status, "{origin} {site}");
    }
    // A sign-in form posted from another site is refused before it is read.
    let response = admin
        .app
        .clone()
        .oneshot(
            Request::builder()
                .method(Method::POST)
                .uri("/api/session")
                .header(header::HOST, "openleet.test")
                .header(header::ORIGIN, "https://evil.example")
                .header(header::CONTENT_TYPE, "application/json")
                .body(Body::from("{}"))
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(response.status(), StatusCode::FORBIDDEN);
}

#[tokio::test]
async fn every_progress_endpoint_needs_a_session() {
    let dir = TempDir::new("accounts-401");
    let state = state(&dir);
    let mut anonymous = Browser::new(&state);
    let body = Some(json!({"slug": "two-sum", "code": "x", "text": "x", "grade": "good"}));
    for (method, uri) in [
        (Method::GET, "/api/deck"),
        (Method::POST, "/api/attempts"),
        (Method::PUT, "/api/notes"),
        (Method::DELETE, "/api/progress?all=true"),
        (Method::GET, "/api/problems"),
        (Method::GET, "/api/problems/two-sum"),
        (Method::GET, "/api/report"),
        (Method::GET, "/api/readiness"),
        (Method::GET, "/api/next"),
        (Method::GET, "/api/plans"),
        (Method::PUT, "/api/plans"),
        (Method::PATCH, "/api/plans/1"),
        (Method::DELETE, "/api/plans/1"),
        (Method::GET, "/api/lists"),
        (Method::POST, "/api/lists"),
        (Method::PATCH, "/api/lists/1"),
        (Method::DELETE, "/api/lists/1"),
        (Method::GET, "/api/code/two-sum"),
        (Method::PUT, "/api/drafts"),
        (Method::POST, "/api/drafts/reset"),
        (Method::POST, "/api/drafts/restore"),
        (Method::POST, "/api/run"),
        (Method::POST, "/api/submit"),
        (Method::GET, "/api/submissions?slug=two-sum"),
        (Method::GET, "/api/submissions/1"),
        (Method::PUT, "/api/account/password"),
        (Method::DELETE, "/api/account"),
        (Method::GET, "/api/admin/settings"),
        (Method::PATCH, "/api/admin/settings"),
    ] {
        let reply = anonymous.send(method.clone(), uri, body.clone()).await;
        assert_eq!(reply.status, StatusCode::UNAUTHORIZED, "{method} {uri}");
        assert_eq!(reply.body, json!({"error": "Sign in to continue"}));
    }
    // Content stays public.
    for uri in [
        "/api/companies",
        "/api/topics",
        "/api/search?q=two%20sum",
        "/api/version",
        "/api/session",
    ] {
        assert_eq!(anonymous.get(uri).await.status, StatusCode::OK, "{uri}");
    }
}

#[tokio::test]
async fn no_account_sees_or_changes_another_accounts_progress() {
    let dir = TempDir::new("accounts-isolation");
    let state = state(&dir);
    let mut admin = Browser::new(&state);
    admin
        .sign_up("admin@example.com", Some(&setup_code(dir.root())))
        .await;
    let mut ada = Browser::new(&state);
    ada.sign_up("ada@example.com", None).await;
    let mut bob = Browser::new(&state);
    bob.sign_up("bob@example.com", None).await;
    // Fresh never does anything: what any account sees before it practices.
    let mut fresh = Browser::new(&state);
    fresh.sign_up("fresh@example.com", None).await;

    let adas = practice(&state, &mut ada, "ada@example.com").await;
    let ada_before = snapshot(&mut ada, &adas).await;
    // Ada's practice shows for Ada.
    let ada_card = ada.get("/api/problems/two-sum").await.body;
    assert_eq!(ada_card["note"], "ada@example.com's note");
    assert!(ada_card["state"].is_object());
    assert_eq!(
        ada.get("/api/code/two-sum").await.body["draft"],
        "# ada@example.com"
    );
    assert_eq!(ada.get("/api/code/two-sum").await.body["solved"], true);
    assert_eq!(
        ada.get("/api/lists").await.body[0]["name"],
        "ada@example.com list"
    );
    assert_eq!(
        ada.get("/api/plans").await.body[0]["name"],
        "ada@example.com plan"
    );
    let own = ada
        .get(&format!("/api/submissions/{}", adas.submission))
        .await;
    assert_eq!(own.body["code"], "# ada@example.com solution");

    // Bob sees exactly what a fresh account sees: nothing of Ada's, even by her ids.
    let bob_view = snapshot(&mut bob, &adas).await;
    let fresh_view = snapshot(&mut fresh, &adas).await;
    for (bob_read, fresh_read) in bob_view.iter().zip(&fresh_view) {
        assert_eq!(bob_read, fresh_read, "{}", bob_read.0);
    }
    let by_uri = |uri: &str| {
        bob_view
            .iter()
            .find(|(u, _, _)| u == uri)
            .map(|(_, status, body)| (*status, body.clone()))
            .unwrap()
    };
    assert_eq!(
        by_uri(&format!("/api/submissions/{}", adas.submission)).0,
        StatusCode::NOT_FOUND
    );
    assert_eq!(by_uri("/api/problems/two-sum").1["note"], Value::Null);
    assert_eq!(by_uri("/api/code/two-sum").1["draft"], Value::Null);
    assert_eq!(by_uri("/api/code/two-sum").1["solved"], false);
    assert_eq!(by_uri("/api/plans").1, json!([]));
    assert_eq!(by_uri("/api/lists").1, json!([]));
    assert_eq!(by_uri("/api/submissions?slug=two-sum").1, json!([]));
    assert_eq!(
        by_uri("/api/report?company=google").1["report"]["graded"],
        0
    );
    let list_rows = by_uri(&format!("/api/problems?list={}", adas.list)).1;
    assert_eq!(list_rows, json!([]), "another account's list id is no list");

    // Bob cannot change or delete Ada's rows by id.
    for (method, uri, body) in [
        (
            Method::PATCH,
            format!("/api/plans/{}", adas.plan),
            json!({"name": "mine now", "pinned": false}),
        ),
        (
            Method::DELETE,
            format!("/api/plans/{}", adas.plan),
            Value::Null,
        ),
        (
            Method::PATCH,
            format!("/api/lists/{}", adas.list),
            json!({"name": "mine now", "slugs": []}),
        ),
        (
            Method::DELETE,
            format!("/api/lists/{}", adas.list),
            Value::Null,
        ),
    ] {
        let body = (!body.is_null()).then_some(body);
        let reply = bob.send(method.clone(), &uri, body).await;
        assert_eq!(reply.status, StatusCode::NOT_FOUND, "{method} {uri}");
    }
    // A restore with nothing of Bob's to restore stays a 400, never Ada's previous version.
    let restore = bob
        .send(
            Method::POST,
            "/api/drafts/restore",
            Some(json!({"slug": "add-two-numbers", "code": ""})),
        )
        .await;
    assert_eq!(restore.status, StatusCode::BAD_REQUEST);

    // Bob practices the same problems, edits his own plan and list, and clears everything.
    let bobs = practice(&state, &mut bob, "bob@example.com").await;
    assert_ne!((bobs.plan, bobs.list), (adas.plan, adas.list));
    bob.ok(
        Method::PATCH,
        &format!("/api/lists/{}", bobs.list),
        Some(json!({"slugs": ["two-sum"]})),
    )
    .await;
    bob.ok(Method::DELETE, &format!("/api/plans/{}", bobs.plan), None)
        .await;
    bob.ok(Method::DELETE, "/api/progress?slug=two-sum", None)
        .await;
    bob.ok(Method::DELETE, "/api/progress?all=true", None).await;
    bob.ok(
        Method::PUT,
        "/api/notes",
        Some(json!({"slug": "two-sum", "text": ""})),
    )
    .await;
    bob.ok(
        Method::PUT,
        "/api/drafts",
        Some(json!({"slug": "two-sum", "code": ""})),
    )
    .await;
    // None of it touched Ada.
    assert_eq!(snapshot(&mut ada, &adas).await, ada_before);

    // Bob deletes his account: his rows go, Ada's stay, his session ends.
    let bob_id = user_id(&state, "bob@example.com");
    assert!(state.store.rows_of(bob_id).unwrap() > 0);
    let deleted = bob
        .send(
            Method::DELETE,
            "/api/account",
            Some(json!({"password": PASSWORD})),
        )
        .await;
    assert_eq!(deleted.status, StatusCode::NO_CONTENT);
    assert_eq!(bob.get("/api/plans").await.status, StatusCode::UNAUTHORIZED);
    assert!(
        state
            .store
            .credentials("bob@example.com")
            .unwrap()
            .is_none()
    );
    assert_eq!(state.store.rows_of(bob_id).unwrap(), 0);
    assert!(
        state
            .store
            .rows_of(user_id(&state, "ada@example.com"))
            .unwrap()
            > 0
    );
    assert_eq!(snapshot(&mut ada, &adas).await, ada_before);
    // The admin cannot delete their account.
    let refused = admin
        .send(
            Method::DELETE,
            "/api/account",
            Some(json!({"password": PASSWORD})),
        )
        .await;
    assert_eq!(refused.status, StatusCode::BAD_REQUEST);
}

#[tokio::test]
async fn the_first_admin_owns_the_progress_from_before_accounts() {
    let dir = TempDir::new("accounts-adopt");
    let state = state(&dir);
    // Rows from before accounts belong to user 1 (migration 7).
    state
        .store
        .save_note(UserId::FIRST_ADMIN, "two-sum", "from before", 1)
        .unwrap();
    let mut admin = Browser::new(&state);
    admin
        .sign_up("admin@example.com", Some(&setup_code(dir.root())))
        .await;
    assert_eq!(
        admin.get("/api/problems/two-sum").await.body["note"],
        "from before"
    );
    let mut member = Browser::new(&state);
    member.sign_up("member@example.com", None).await;
    assert_eq!(
        member.get("/api/problems/two-sum").await.body["note"],
        Value::Null
    );
}

#[tokio::test]
async fn progress_pages_need_a_session_and_answers_stay_private() {
    let dir = TempDir::new("accounts-pages");
    let state = state(&dir);
    let mut admin = Browser::new(&state);
    admin
        .sign_up("admin@example.com", Some(&setup_code(dir.root())))
        .await;
    let response = admin
        .app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/api/plans")
                .header(header::COOKIE, admin.cookie.clone().unwrap())
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();
    assert_eq!(response.headers()[header::CACHE_CONTROL], "private");
    assert!(
        response
            .headers()
            .get_all(header::VARY)
            .iter()
            .any(|v| v == "cookie")
    );
}

#[tokio::test]
async fn wrong_passwords_from_elsewhere_do_not_lock_the_owner_out() {
    let dir = TempDir::new("accounts-lockout");
    let state = state(&dir);
    let mut admin = Browser::new(&state);
    admin
        .sign_up("admin@example.com", Some(&setup_code(dir.root())))
        .await;
    let mut attacker = Browser::new(&state);
    attacker.address = "198.51.100.7:40000".parse().unwrap();
    for _ in 0..10 {
        assert_eq!(
            attacker
                .sign_in("admin@example.com", "guess guess")
                .await
                .status,
            StatusCode::UNAUTHORIZED
        );
    }
    // The attacker's address is locked out of this account, even with the right password.
    assert_eq!(
        attacker.sign_in("admin@example.com", PASSWORD).await.status,
        StatusCode::TOO_MANY_REQUESTS
    );
    // The owner, elsewhere, signs in.
    let mut owner = Browser::new(&state);
    assert_eq!(
        owner.sign_in("admin@example.com", PASSWORD).await.status,
        StatusCode::OK
    );
    // Wrong current passwords count against the signed-in account itself.
    for _ in 0..10 {
        let reply = owner
            .send(
                Method::PUT,
                "/api/account/password",
                Some(json!({"current": "guess guess", "password": "a new password"})),
            )
            .await;
        assert_eq!(reply.status, StatusCode::FORBIDDEN);
    }
    let reply = owner
        .send(
            Method::PUT,
            "/api/account/password",
            Some(json!({"current": PASSWORD, "password": "a new password"})),
        )
        .await;
    assert_eq!(reply.status, StatusCode::TOO_MANY_REQUESTS);
}

#[tokio::test]
async fn signing_in_again_ends_the_browsers_old_session() {
    let dir = TempDir::new("accounts-again");
    let state = state(&dir);
    let mut admin = Browser::new(&state);
    admin
        .sign_up("admin@example.com", Some(&setup_code(dir.root())))
        .await;
    let old = admin.cookie.clone();
    assert_eq!(
        admin.sign_in("admin@example.com", PASSWORD).await.status,
        StatusCode::OK
    );
    assert_ne!(admin.cookie, old);
    let mut stale = Browser::new(&state);
    stale.cookie = old;
    assert_eq!(
        stale.get("/api/plans").await.status,
        StatusCode::UNAUTHORIZED
    );
    assert_eq!(state.store.sessions(0).unwrap().len(), 1);
}

#[tokio::test]
async fn a_deleted_account_gets_no_session_or_write_again() {
    let dir = TempDir::new("accounts-deleted");
    let state = state(&dir);
    let mut admin = Browser::new(&state);
    admin
        .sign_up("admin@example.com", Some(&setup_code(dir.root())))
        .await;
    let mut ada = Browser::new(&state);
    ada.sign_up("ada@example.com", None).await;
    let ada_id = user_id(&state, "ada@example.com");
    let me = crate::auth::Me::test(&state, ada_id).await;
    ada.send(
        Method::DELETE,
        "/api/account",
        Some(json!({"password": PASSWORD})),
    )
    .await;
    // A request that got past the session check before the delete writes nothing.
    let late = state
        .update_progress(&me.learner, |state, learner| {
            state.store.save_draft(learner.user, "two-sum", "late", 1)
        })
        .await;
    assert!(matches!(late, Err(crate::error::ApiError::SignIn)));
    assert!(matches!(
        state.learner(ada_id).await,
        Err(crate::error::ApiError::SignIn)
    ));
    let user = crate::db::User {
        id: ada_id,
        email: "ada@example.com".into(),
        admin: false,
    };
    assert!(
        state
            .auth
            .start_session(&state.store, user, crate::state::now_ms())
            .is_err()
    );
    assert_eq!(state.store.rows_of(ada_id).unwrap(), 0);
    // The email is free again, for a new account with a new id.
    let mut again = Browser::new(&state);
    assert_eq!(
        again.sign_up("ada@example.com", None).await.status,
        StatusCode::CREATED
    );
    assert_ne!(user_id(&state, "ada@example.com"), ada_id);
}
