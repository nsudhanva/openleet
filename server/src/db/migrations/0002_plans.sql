-- Migration 2: practice plans, remembered as they are used.
--
-- Conventions as in 0001_progress.sql. A plan is a problem list (company and period), filters
-- (topic, difficulty), which of its problems still count (status) and an order; the server
-- builds its problems on the fly from the static content, so a row holds only those values,
-- in the API's spellings, plus what the learner made of it (a name, a pin).
--
-- One row per distinct plan. That is not a UNIQUE constraint (an ART index, which costs
-- memory under the 64 MB limit): the server upserts plans one at a time, under the lock that
-- serializes progress writes (AppState::update_progress), matching an existing row with
-- IS NOT DISTINCT FROM, so NULL topics and difficulties match too (Store::upsert_plan). The
-- table stays tiny: at most 8 unpinned rows (the least recently used go) and 50 pinned.

CREATE TYPE plan_status AS ENUM ('unsolved', 'untried', 'all');
COMMENT ON TYPE plan_status IS 'Which problems of a plan still count: unsolved (no accepted submission), untried (no submission) or all.';

CREATE TYPE plan_order AS ENUM ('rank', 'number', 'easy-first', 'random');
COMMENT ON TYPE plan_order IS 'The order a plan walks its problems in: rank (list order), number (LeetCode number), easy-first (difficulty, then rank) or random (a shuffle seeded by the plan).';

CREATE SEQUENCE plan_id_seq START 1;
COMMENT ON SEQUENCE plan_id_seq IS 'Ids of plans.id, in the order plans are first used.';

CREATE TABLE plans (
    id BIGINT PRIMARY KEY DEFAULT nextval('plan_id_seq'),
    company VARCHAR NOT NULL CHECK (company <> ''),
    period VARCHAR NOT NULL CHECK (period IN ('30d', '3m', '6m', 'all', 'lc1000')),
    topic VARCHAR CHECK (topic <> ''),
    difficulty VARCHAR CHECK (difficulty IN ('Easy', 'Medium', 'Hard')),
    status plan_status NOT NULL,
    sort_order plan_order NOT NULL,
    name VARCHAR CHECK (length(name) BETWEEN 1 AND 60),
    pinned BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL,
    used_at TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE plans IS 'Practice plans the learner used, pinned or recent: one row per distinct plan (enforced by the server''s upsert, not by a constraint).';
COMMENT ON COLUMN plans.id IS 'Surrogate key from plan_id_seq; the API''s plan id.';
COMMENT ON COLUMN plans.company IS 'The list''s company slug, or any; ignored for the lc1000 period.';
COMMENT ON COLUMN plans.period IS 'The list''s period: 30d, 3m, 6m, all or lc1000.';
COMMENT ON COLUMN plans.topic IS 'Only problems with this topic tag; NULL for any topic.';
COMMENT ON COLUMN plans.difficulty IS 'Only problems of this difficulty; NULL for any.';
COMMENT ON COLUMN plans.status IS 'Which problems still count.';
COMMENT ON COLUMN plans.sort_order IS 'The order the plan walks its problems in.';
COMMENT ON COLUMN plans.name IS 'The learner''s name for the plan, trimmed, 1 to 60 characters; NULL shows its label.';
COMMENT ON COLUMN plans.pinned IS 'Whether the learner pinned it; pinned plans are kept, unpinned ones only while recent.';
COMMENT ON COLUMN plans.created_at IS 'When the plan was first used.';
COMMENT ON COLUMN plans.used_at IS 'When the plan was last used (or unpinned), for the recent list.';
