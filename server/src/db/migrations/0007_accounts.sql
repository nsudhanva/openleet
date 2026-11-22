-- Migration 7: accounts. Each person signs in with an email and a password, and every row of
-- progress belongs to one account (user_id). Rows from before accounts belong to user 1, the
-- first admin, who claims them with the server's one-time setup code (server/src/auth.rs).
--
-- user_id has no FOREIGN KEY: DuckDB has no ON DELETE CASCADE, and each foreign key adds an
-- ART index on a large table. The server writes a user's rows only for a signed-in user, and
-- deletes them in the transaction that deletes the user. Every read and write filters on
-- user_id, so no query reaches another account's rows.

CREATE SEQUENCE user_id_seq START 2;
COMMENT ON SEQUENCE user_id_seq IS 'Ids of users.id for accounts made by sign-up. Id 1 is kept for the first admin, who owns the progress from before accounts.';

CREATE TABLE users (
    id BIGINT PRIMARY KEY DEFAULT nextval('user_id_seq'),
    email VARCHAR NOT NULL UNIQUE CHECK (length(email) BETWEEN 3 AND 254 AND contains(email, '@')),
    password_hash VARCHAR NOT NULL CHECK (starts_with(password_hash, '$argon2id$')),
    admin BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL,
    password_changed_at TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE users IS 'Accounts: one per email. Progress rows name their account in user_id.';
COMMENT ON COLUMN users.id IS 'Surrogate key; 1 is the first admin, made with the setup code, the rest come from user_id_seq.';
COMMENT ON COLUMN users.email IS 'The sign-in email, trimmed and lowercased by the server, so each address has one account. Never verified.';
COMMENT ON COLUMN users.password_hash IS 'Argon2id PHC string (algorithm, parameters, random salt and hash); the password itself is never stored.';
COMMENT ON COLUMN users.admin IS 'Whether the account can change the server settings (whether sign-ups are open).';
COMMENT ON COLUMN users.created_at IS 'When the account was made.';
COMMENT ON COLUMN users.password_changed_at IS 'When the password was last set; a change ends the account''s other sessions.';

CREATE TABLE sessions (
    token_hash BLOB PRIMARY KEY CHECK (octet_length(token_hash) = 32),
    user_id BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    CHECK (expires_at > created_at)
);
COMMENT ON TABLE sessions IS 'Signed-in browsers. The cookie holds a random 256-bit token; only its SHA-256 is stored, so this table (or a backup of it) cannot sign anyone in.';
COMMENT ON COLUMN sessions.token_hash IS 'SHA-256 of the session token.';
COMMENT ON COLUMN sessions.user_id IS 'The signed-in account (users.id).';
COMMENT ON COLUMN sessions.created_at IS 'When the account signed in.';
COMMENT ON COLUMN sessions.expires_at IS 'When the session ends unless used; each day of use moves it 30 days on.';

CREATE TABLE settings (
    id BOOLEAN PRIMARY KEY DEFAULT true CHECK (id),
    signups_open BOOLEAN NOT NULL
);
COMMENT ON TABLE settings IS 'Server settings an admin can change: exactly one row.';
COMMENT ON COLUMN settings.id IS 'Always true, so the table holds one row.';
COMMENT ON COLUMN settings.signups_open IS 'Whether anyone can make an account. The first admin can always claim the setup code.';
INSERT INTO settings (id, signups_open) VALUES (true, true);

-- Tables keyed by id gain an owner.
ALTER TABLE attempts ADD COLUMN user_id BIGINT DEFAULT 1;
ALTER TABLE attempts ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE attempts ALTER COLUMN user_id DROP DEFAULT;
COMMENT ON COLUMN attempts.user_id IS 'The account that answered (users.id).';

ALTER TABLE submissions ADD COLUMN user_id BIGINT DEFAULT 1;
ALTER TABLE submissions ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE submissions ALTER COLUMN user_id DROP DEFAULT;
COMMENT ON COLUMN submissions.user_id IS 'The account that submitted (users.id). The API shows a submission to its account only.';
COMMENT ON TABLE submissions IS 'Judged submissions, append-only. Only the newest 100 per account and problem, and the latest accepted one, keep their code and detail.';

ALTER TABLE plans ADD COLUMN user_id BIGINT DEFAULT 1;
ALTER TABLE plans ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE plans ALTER COLUMN user_id DROP DEFAULT;
COMMENT ON COLUMN plans.user_id IS 'The account that used the plan (users.id).';
COMMENT ON TABLE plans IS 'Practice plans each account used, pinned or recent: one row per account and distinct plan (enforced by the server''s upsert, not by a constraint).';

ALTER TABLE user_lists ADD COLUMN user_id BIGINT DEFAULT 1;
ALTER TABLE user_lists ALTER COLUMN user_id SET NOT NULL;
ALTER TABLE user_lists ALTER COLUMN user_id DROP DEFAULT;
COMMENT ON COLUMN user_lists.user_id IS 'The account that made the list (users.id); its problems (user_list_problems) belong to it too.';

-- Tables keyed by problem become keyed by account and problem: DuckDB cannot change a
-- primary key, so each is rebuilt and renamed.
CREATE TABLE notes_by_user (
    user_id BIGINT NOT NULL,
    slug VARCHAR NOT NULL CHECK (slug <> ''),
    body VARCHAR NOT NULL CHECK (body <> ''),
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (user_id, slug)
);
INSERT INTO notes_by_user SELECT 1, slug, body, updated_at FROM notes;
DROP TABLE notes;
ALTER TABLE notes_by_user RENAME TO notes;
COMMENT ON TABLE notes IS 'Each account''s own answer per problem; saving an empty answer deletes the row.';
COMMENT ON COLUMN notes.user_id IS 'The account (users.id).';
COMMENT ON COLUMN notes.slug IS 'The problem.';
COMMENT ON COLUMN notes.body IS 'The answer text, trimmed and never empty.';
COMMENT ON COLUMN notes.updated_at IS 'When the answer was last saved.';

CREATE TABLE drafts_by_user (
    user_id BIGINT NOT NULL,
    slug VARCHAR NOT NULL CHECK (slug <> ''),
    code VARCHAR CHECK (code <> ''),
    previous_code VARCHAR CHECK (previous_code <> ''),
    updated_at TIMESTAMPTZ NOT NULL,
    PRIMARY KEY (user_id, slug),
    CHECK (code IS NOT NULL OR previous_code IS NOT NULL)
);
INSERT INTO drafts_by_user SELECT 1, slug, code, previous_code, updated_at FROM drafts;
DROP TABLE drafts;
ALTER TABLE drafts_by_user RENAME TO drafts;
COMMENT ON TABLE drafts IS 'Editor code per account and problem. A row exists only while it holds code or a previous version.';
COMMENT ON COLUMN drafts.user_id IS 'The account (users.id).';
COMMENT ON COLUMN drafts.slug IS 'The problem.';
COMMENT ON COLUMN drafts.code IS 'The code in the editor; NULL means the starter code.';
COMMENT ON COLUMN drafts.previous_code IS 'What the last Reset or Restore replaced, for Restore; NULL when there is none.';
COMMENT ON COLUMN drafts.updated_at IS 'When the draft last changed.';

CREATE TABLE daily_scores_by_user (
    user_id BIGINT NOT NULL,
    scored_on DATE NOT NULL,
    computed_at TIMESTAMPTZ NOT NULL,
    readiness DOUBLE NOT NULL CHECK (readiness BETWEEN 0 AND 1),
    coverage DOUBLE NOT NULL CHECK (coverage BETWEEN 0 AND 1),
    accuracy DOUBLE CHECK (accuracy BETWEEN 0 AND 1),
    PRIMARY KEY (user_id, scored_on)
);
INSERT INTO daily_scores_by_user
    SELECT 1, scored_on, computed_at, readiness, coverage, accuracy FROM daily_scores;
DROP TABLE daily_scores;
ALTER TABLE daily_scores_by_user RENAME TO daily_scores;
COMMENT ON TABLE daily_scores IS 'Readiness snapshots from releases before migration 4, all of user 1: one row per day the background scorer ran once anything was graded. Neither written nor read now; clearing all progress deletes the account''s rows.';
COMMENT ON COLUMN daily_scores.user_id IS 'The account (users.id).';
COMMENT ON COLUMN daily_scores.scored_on IS 'The calendar day, in the server''s time zone.';
COMMENT ON COLUMN daily_scores.computed_at IS 'When the day''s latest scores were computed.';
COMMENT ON COLUMN daily_scores.readiness IS 'The default company''s readiness under the formula of that time: a frequency-weighted mean of flashcard mastery (topic guess and self-grade, faded since the last review) over its 6-month list, in [0, 1].';
COMMENT ON COLUMN daily_scores.coverage IS 'Share of that list graded at least once, in [0, 1].';
COMMENT ON COLUMN daily_scores.accuracy IS 'Mean topic score of the last 50 graded attempts, in [0, 1]; NULL when there were none.';
