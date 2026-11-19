-- Migration 6: the learner's own problem lists, hand-picked and named.
--
-- A list holds problems by slug, in the order they were added; a practice plan can walk one
-- instead of a company list (the API's `list` parameter). Like plans, the server keeps every
-- list in memory and writes one at a time under the lock that serializes progress writes,
-- which keeps each slug once per list (no UNIQUE constraint, whose ART index costs memory).

CREATE SEQUENCE user_list_id_seq START 1;
COMMENT ON SEQUENCE user_list_id_seq IS 'Ids of user_lists.id, in the order lists are created.';

CREATE TABLE user_lists (
    id BIGINT PRIMARY KEY DEFAULT nextval('user_list_id_seq'),
    name VARCHAR NOT NULL CHECK (length(name) BETWEEN 1 AND 60),
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
);
COMMENT ON TABLE user_lists IS 'Problem lists the learner made: a name over hand-picked problems (user_list_problems).';
COMMENT ON COLUMN user_lists.id IS 'Surrogate key from user_list_id_seq; the API''s list id.';
COMMENT ON COLUMN user_lists.name IS 'The learner''s name for the list, trimmed, 1 to 60 characters.';
COMMENT ON COLUMN user_lists.created_at IS 'When the list was made.';
COMMENT ON COLUMN user_lists.updated_at IS 'When its name or problems last changed.';

CREATE TABLE user_list_problems (
    list_id BIGINT NOT NULL,
    slug VARCHAR NOT NULL CHECK (slug <> ''),
    position INTEGER NOT NULL CHECK (position >= 0)
);
COMMENT ON TABLE user_list_problems IS 'The problems of each user list, one row per problem (each slug once per list, kept by the server).';
COMMENT ON COLUMN user_list_problems.list_id IS 'The list (user_lists.id); its rows go when the list is deleted.';
COMMENT ON COLUMN user_list_problems.slug IS 'The problem (data/problems.json).';
COMMENT ON COLUMN user_list_problems.position IS 'Where the problem sits in the list, from 0: the order the learner added problems in.';
