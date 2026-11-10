-- Adopting an unversioned database, part 1 of 2: runs in the same transaction as migration 1
-- and legacy_adopt.sql, before migration 1.
--
-- Unversioned databases were made by `CREATE ... IF NOT EXISTS` statements that grew over time,
-- so first bring an older one up to their last form (the statements below, frozen), then
-- move every row aside into temporary tables with plain types, and drop the old tables, types
-- and sequence so migration 1 can create the clean ones under the same names.

CREATE TYPE IF NOT EXISTS grade AS ENUM ('again', 'good', 'less', 'skip');
CREATE TYPE IF NOT EXISTS verdict AS ENUM ('accepted', 'wrong_answer', 'time_limit_exceeded',
    'memory_limit_exceeded', 'runtime_error', 'compile_error', 'output_limit_exceeded',
    'internal_error');
CREATE SEQUENCE IF NOT EXISTS submission_id START 1;
CREATE TABLE IF NOT EXISTS attempts (slug VARCHAR NOT NULL, at_ms BIGINT NOT NULL,
    grade grade NOT NULL, guessed VARCHAR[] NOT NULL, score DOUBLE, hints UTINYINT NOT NULL);
CREATE TABLE IF NOT EXISTS daily_scores (day DATE PRIMARY KEY, at_ms BIGINT NOT NULL,
    readiness DOUBLE NOT NULL, coverage DOUBLE NOT NULL, accuracy DOUBLE);
CREATE TABLE IF NOT EXISTS notes (slug VARCHAR PRIMARY KEY, text VARCHAR NOT NULL,
    at_ms BIGINT NOT NULL);
CREATE TABLE IF NOT EXISTS drafts (slug VARCHAR PRIMARY KEY, code VARCHAR NOT NULL,
    at_ms BIGINT NOT NULL, previous VARCHAR);
ALTER TABLE drafts ADD COLUMN IF NOT EXISTS previous VARCHAR;
CREATE TABLE IF NOT EXISTS submissions (id BIGINT PRIMARY KEY DEFAULT nextval('submission_id'),
    slug VARCHAR NOT NULL, at_ms BIGINT NOT NULL, code VARCHAR NOT NULL,
    verdict verdict NOT NULL, passed USMALLINT NOT NULL, total USMALLINT NOT NULL,
    cpu_ms UINTEGER NOT NULL, detail VARIANT);

-- The log had no key: rowid keeps the insertion order among attempts at the same millisecond.
CREATE TEMP TABLE legacy_attempts AS
    SELECT rowid AS seq, slug, at_ms, grade::VARCHAR AS grade, guessed, score, hints
    FROM attempts;
CREATE TEMP TABLE legacy_daily_scores AS FROM daily_scores;
CREATE TEMP TABLE legacy_notes AS FROM notes;
CREATE TEMP TABLE legacy_drafts AS FROM drafts;
CREATE TEMP TABLE legacy_submissions AS
    SELECT * REPLACE (verdict::VARCHAR AS verdict) FROM submissions;

DROP TABLE attempts;
DROP TABLE daily_scores;
DROP TABLE notes;
DROP TABLE drafts;
DROP TABLE submissions;
DROP TYPE grade;
DROP TYPE verdict;
DROP SEQUENCE submission_id;
