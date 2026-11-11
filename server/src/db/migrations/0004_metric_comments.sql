-- Migration 4: comments only, every row stays. The progress page computes readiness and its
-- trend from attempts and submissions, so nothing writes or reads daily_scores any more; its
-- rows are kept as data (clearing all progress still deletes them). A shaky solve now clears
-- on a clean solve on a later day.

COMMENT ON TABLE daily_scores IS 'Readiness snapshots from releases before migration 4: one row per day the background scorer ran once anything was graded, whether or not you practiced that day. Neither written nor read now; clearing all progress deletes it.';
COMMENT ON COLUMN daily_scores.readiness IS 'The default company''s readiness under the formula of that time: a frequency-weighted mean of flashcard mastery (topic guess and self-grade, faded since the last review) over its 6-month list, in [0, 1].';
COMMENT ON COLUMN daily_scores.coverage IS 'Share of that list graded at least once, in [0, 1].';
COMMENT ON COLUMN daily_scores.accuracy IS 'Mean topic score of the last 50 graded attempts, in [0, 1]; NULL when there were none.';

COMMENT ON TYPE plan_status IS 'Which problems of a plan still count: unsolved (no accepted submission), untried (no submission), all, or shaky (accepted only after two or more wrong answers, limits or crashes, or a time limit, and not since solved again cleanly on a later day; the server decides which, from the submissions).';
