-- Migration 1: the progress schema.
--
-- Conventions: snake_case; *_at columns are TIMESTAMPTZ instants and *_on columns calendar
-- dates. The API still speaks Unix milliseconds: writes bind to_timestamp(ms / 1000), reads
-- select epoch_ms(column). Both are core functions (the server loads no ICU extension) that
-- involve no time zone, and the round trip is exact: a millisecond count over 1000 is within
-- 0.3 microseconds as a double for any date before 2200, and to_timestamp rounds to the
-- microsecond. Every slug names a problem of data/problems.json. Problems
-- are static content shipped with the release, not rows here, so slugs carry no foreign key.
--
-- No secondary indexes. The server reads attempts, notes and the solved set into memory once
-- at startup (full scans) and serves every hot read from memory; the remaining queries touch
-- one user's rows (hundreds to a few thousand): drafts and notes by primary key, submissions
-- by id (primary key) or by slug, newest first, where a scan of a table this size costs well
-- under a millisecond and min-max zone maps on the insertion-ordered id and time columns
-- already prune row groups. An ART index would cost memory under a 64 MB limit for nothing.

CREATE TYPE grade AS ENUM ('again', 'good', 'less', 'skip');
COMMENT ON TYPE grade IS 'A flashcard answer''s outcome: again (forgotten), good, less (show it less often) or skip (not graded).';

CREATE TYPE verdict AS ENUM (
    'accepted', 'wrong_answer', 'time_limit_exceeded', 'memory_limit_exceeded',
    'runtime_error', 'compile_error', 'output_limit_exceeded', 'internal_error'
);
COMMENT ON TYPE verdict IS 'The judge''s verdict on a submission; the names of openleet_proto::Verdict.';

CREATE SEQUENCE attempt_id_seq START 1;
COMMENT ON SEQUENCE attempt_id_seq IS 'Ids of attempts.id, in the order attempts are recorded.';

CREATE SEQUENCE submission_id_seq START 1;
COMMENT ON SEQUENCE submission_id_seq IS 'Ids of submissions.id, in the order submissions are judged.';

CREATE TABLE attempts (
    id BIGINT PRIMARY KEY DEFAULT nextval('attempt_id_seq'),
    slug VARCHAR NOT NULL CHECK (slug <> ''),
    answered_at TIMESTAMPTZ NOT NULL,
    grade grade NOT NULL,
    guessed_topics VARCHAR[] NOT NULL,
    topic_score DOUBLE CHECK (topic_score BETWEEN 0 AND 1),
    hints_used UTINYINT NOT NULL CHECK (hints_used <= 10),
    CHECK ((grade = 'skip') = (topic_score IS NULL))
);
COMMENT ON TABLE attempts IS 'The flashcard log, append-only: one row per graded or skipped card. Card states and reports are replayed from it.';
COMMENT ON COLUMN attempts.id IS 'Surrogate key from attempt_id_seq; also the replay order for attempts with the same answered_at.';
COMMENT ON COLUMN attempts.slug IS 'The problem answered.';
COMMENT ON COLUMN attempts.answered_at IS 'When the answer was recorded.';
COMMENT ON COLUMN attempts.grade IS 'The learner''s grade, or skip.';
COMMENT ON COLUMN attempts.guessed_topics IS 'Topics the learner guessed, in the order given; empty for skips.';
COMMENT ON COLUMN attempts.topic_score IS 'F1 of guessed_topics against the problem''s topics, in [0, 1]; NULL exactly for skips.';
COMMENT ON COLUMN attempts.hints_used IS 'Hints opened before answering (the API allows at most 10).';

CREATE TABLE daily_scores (
    scored_on DATE PRIMARY KEY,
    computed_at TIMESTAMPTZ NOT NULL,
    readiness DOUBLE NOT NULL CHECK (readiness BETWEEN 0 AND 1),
    coverage DOUBLE NOT NULL CHECK (coverage BETWEEN 0 AND 1),
    accuracy DOUBLE CHECK (accuracy BETWEEN 0 AND 1)
);
COMMENT ON TABLE daily_scores IS 'One row per day with practice: the default company''s scores, for the progress chart. Each refresh replaces the day''s row.';
COMMENT ON COLUMN daily_scores.scored_on IS 'The calendar day, in the server''s time zone.';
COMMENT ON COLUMN daily_scores.computed_at IS 'When the day''s latest scores were computed.';
COMMENT ON COLUMN daily_scores.readiness IS 'Weighted mean recall probability over the problems in scope, in [0, 1].';
COMMENT ON COLUMN daily_scores.coverage IS 'Share of the problems in scope attempted at least once, in [0, 1].';
COMMENT ON COLUMN daily_scores.accuracy IS 'Mean topic score of recent attempts, in [0, 1]; NULL when there are none.';

CREATE TABLE notes (
    slug VARCHAR PRIMARY KEY CHECK (slug <> ''),
    body VARCHAR NOT NULL CHECK (body <> ''),
    updated_at TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE notes IS 'The learner''s own answer per problem; saving an empty answer deletes the row.';
COMMENT ON COLUMN notes.slug IS 'The problem.';
COMMENT ON COLUMN notes.body IS 'The answer text, trimmed and never empty.';
COMMENT ON COLUMN notes.updated_at IS 'When the answer was last saved.';

CREATE TABLE drafts (
    slug VARCHAR PRIMARY KEY CHECK (slug <> ''),
    code VARCHAR CHECK (code <> ''),
    previous_code VARCHAR CHECK (previous_code <> ''),
    updated_at TIMESTAMPTZ NOT NULL,
    CHECK (code IS NOT NULL OR previous_code IS NOT NULL)
);
COMMENT ON TABLE drafts IS 'Editor code per problem. A row exists only while it holds code or a previous version.';
COMMENT ON COLUMN drafts.slug IS 'The problem.';
COMMENT ON COLUMN drafts.code IS 'The code in the editor; NULL means the starter code.';
COMMENT ON COLUMN drafts.previous_code IS 'What the last Reset or Restore replaced, for Restore; NULL when there is none.';
COMMENT ON COLUMN drafts.updated_at IS 'When the draft last changed.';

CREATE TABLE submissions (
    id BIGINT PRIMARY KEY DEFAULT nextval('submission_id_seq'),
    slug VARCHAR NOT NULL CHECK (slug <> ''),
    submitted_at TIMESTAMPTZ NOT NULL,
    code VARCHAR NOT NULL,
    verdict verdict NOT NULL,
    tests_passed USMALLINT NOT NULL,
    tests_total USMALLINT NOT NULL,
    cpu_ms UINTEGER NOT NULL,
    detail VARIANT,
    CHECK (tests_passed <= tests_total)
);
COMMENT ON TABLE submissions IS 'Judged submissions, append-only.';
COMMENT ON COLUMN submissions.id IS 'Surrogate key from submission_id_seq; the API''s submission id.';
COMMENT ON COLUMN submissions.slug IS 'The problem.';
COMMENT ON COLUMN submissions.submitted_at IS 'When the submission was judged.';
COMMENT ON COLUMN submissions.code IS 'The submitted source code.';
COMMENT ON COLUMN submissions.verdict IS 'The judge''s verdict.';
COMMENT ON COLUMN submissions.tests_passed IS 'Tests passed before the first failure (all of them when accepted).';
COMMENT ON COLUMN submissions.tests_total IS 'Tests the problem has.';
COMMENT ON COLUMN submissions.cpu_ms IS 'CPU time used, in milliseconds.';
COMMENT ON COLUMN submissions.detail IS 'What the result page shows (failing case, error, limits); its shape depends on the verdict.';
