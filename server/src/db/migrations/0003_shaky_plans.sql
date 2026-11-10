-- Migration 3: plans can keep the shaky solves (status 'shaky': solved, but only after two or
-- more failed submissions or a time limit; the server decides which, from the submissions).
--
-- DuckDB cannot add a value to an ENUM type in place, so the column goes through VARCHAR while
-- the type is recreated with the new value; every row keeps its status.

ALTER TABLE plans ALTER status TYPE VARCHAR;
DROP TYPE plan_status;
CREATE TYPE plan_status AS ENUM ('unsolved', 'untried', 'all', 'shaky');
COMMENT ON TYPE plan_status IS 'Which problems of a plan still count: unsolved (no accepted submission), untried (no submission), all, or shaky (accepted only after two or more failed submissions or a time limit).';
ALTER TABLE plans ALTER status TYPE plan_status;
COMMENT ON COLUMN plans.status IS 'Which problems still count.';
