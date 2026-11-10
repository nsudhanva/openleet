-- Moves each id sequence past the largest id in its table, after rows were inserted with
-- explicit ids (adopting an unversioned database, restoring a backup). DuckDB has no setval,
-- so this draws the missing values; duckdb_sequences() gives the last one drawn.

SELECT max(nextval('attempt_id_seq')) FROM range(
    (SELECT coalesce(max(id), 0) FROM attempts)
    - (SELECT coalesce(last_value, start_value - 1) FROM duckdb_sequences()
       WHERE database_name = current_database() AND sequence_name = 'attempt_id_seq'));

SELECT max(nextval('submission_id_seq')) FROM range(
    (SELECT coalesce(max(id), 0) FROM submissions)
    - (SELECT coalesce(last_value, start_value - 1) FROM duckdb_sequences()
       WHERE database_name = current_database() AND sequence_name = 'submission_id_seq'));
