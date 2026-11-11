-- Migration 5: every submission stays, since the coding analytics are replayed from them at
-- startup. To save space, a problem's older submissions lose only their code and detail (the
-- server keeps those for its newest 100 and its latest accepted one).

ALTER TABLE submissions ALTER code DROP NOT NULL;
COMMENT ON TABLE submissions IS 'Judged submissions, append-only. Only each problem''s newest 100 and its latest accepted one keep their code and detail.';
COMMENT ON COLUMN submissions.code IS 'The submitted source code; NULL once dropped for space.';
COMMENT ON COLUMN submissions.detail IS 'What the result page shows (failing case, error, limits); its shape depends on the verdict. NULL once dropped for space.';
