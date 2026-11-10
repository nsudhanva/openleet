-- Adopting an unversioned database, part 2 of 2: runs right after migration 1, in the same
-- transaction, and moves the rows legacy_stage.sql set aside into the clean tables.
--
-- Every value is kept; epoch milliseconds become TIMESTAMPTZ exactly (see 0001_progress.sql).
-- The only rows not carried over are ones the old code meant as "nothing":
-- an empty note (saving one deleted it) and a draft holding neither code nor a previous
-- version (the old code deleted those right after writing them).

INSERT INTO attempts (id, slug, answered_at, grade, guessed_topics, topic_score, hints_used)
SELECT row_number() OVER (ORDER BY at_ms, seq), slug, to_timestamp(at_ms / 1000), grade,
    guessed, score, hints
FROM temp.legacy_attempts;

INSERT INTO daily_scores (scored_on, computed_at, readiness, coverage, accuracy)
SELECT day, to_timestamp(at_ms / 1000), readiness, coverage, accuracy
FROM temp.legacy_daily_scores;

INSERT INTO notes (slug, body, updated_at)
SELECT slug, text, to_timestamp(at_ms / 1000)
FROM temp.legacy_notes
WHERE text <> '';

INSERT INTO drafts (slug, code, previous_code, updated_at)
SELECT slug, nullif(code, ''), nullif(previous, ''), to_timestamp(at_ms / 1000)
FROM temp.legacy_drafts
WHERE nullif(code, '') IS NOT NULL OR nullif(previous, '') IS NOT NULL;

INSERT INTO submissions (id, slug, submitted_at, code, verdict, tests_passed, tests_total,
    cpu_ms, detail)
SELECT id, slug, to_timestamp(at_ms / 1000), code, verdict, passed, total, cpu_ms, detail
FROM temp.legacy_submissions;

DROP TABLE temp.legacy_attempts;
DROP TABLE temp.legacy_daily_scores;
DROP TABLE temp.legacy_notes;
DROP TABLE temp.legacy_drafts;
DROP TABLE temp.legacy_submissions;
