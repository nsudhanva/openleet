import json
import tempfile
import unittest
from pathlib import Path

import duckdb

from openleet.judging.testdb import write_jsonl


class TestDbTests(unittest.TestCase):
    def test_writer_creates_compressed_json_columns_without_primary_key(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            staging = tmp_path / "tests.jsonl"
            staging.write_text(
                json.dumps(
                    {
                        "slug": "sample",
                        "idx": 0,
                        "kind": "example",
                        "test_case": '{"input":{}}',
                        "expected": "1",
                        "expected_sha256": None,
                    }
                )
                + "\n"
            )
            corpus = tmp_path / "tests.duckdb"
            write_jsonl(corpus, staging, "test")

            with duckdb.connect(str(corpus), read_only=True) as con:
                columns = con.execute(
                    "SELECT column_name, data_type, is_nullable FROM information_schema.columns "
                    "WHERE table_name = 'tests'"
                ).fetchall()
                primary_keys = con.execute(
                    "SELECT count(*) FROM duckdb_constraints() "
                    "WHERE table_name = 'tests' AND constraint_type = 'PRIMARY KEY'"
                ).fetchone()[0]
                row = con.execute(
                    "SELECT test_case::VARCHAR, expected::VARCHAR FROM tests"
                ).fetchone()
                storage = con.execute("PRAGMA storage_info('tests')").fetchall()

        self.assertIn(("test_case", "JSON", "NO"), columns)
        self.assertIn(("expected", "JSON", "YES"), columns)
        self.assertEqual(primary_keys, 0)
        self.assertEqual(row, ('{"input":{}}', "1"))
        self.assertEqual(
            {row[1] for row in storage if row[5] != "VALIDITY" and row[8] == "ZSTD"},
            {"test_case", "expected"},
        )

    def test_gap_validation_rejects_duplicate_indexes_with_a_gap(self):
        with tempfile.TemporaryDirectory() as directory:
            tmp_path = Path(directory)
            staging = tmp_path / "tests.jsonl"
            rows = [
                {
                    "slug": "sample",
                    "idx": idx,
                    "kind": "example",
                    "test_case": "{}",
                    "expected": "1",
                    "expected_sha256": None,
                }
                for idx in (0, 0, 2)
            ]
            staging.write_text("".join(json.dumps(row) + "\n" for row in rows))

            with self.assertRaises(SystemExit):
                write_jsonl(tmp_path / "tests.duckdb", staging, "test")
