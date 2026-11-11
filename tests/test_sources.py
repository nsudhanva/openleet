import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import duckdb

from openleet.judging import sources


class SourcesTests(unittest.TestCase):
    def test_mercury_reads_parquet_paths_as_parameters(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "quoted'path.parquet"
            literal = "'" + str(path).replace("'", "''") + "'"
            with duckdb.connect() as con:
                con.execute(
                    "COPY (SELECT 'sample' AS slug_name, "
                    "[{'runtime': '1 ms', 'solution': 'class Solution: pass'}] AS solutions) "
                    f"TO {literal} (FORMAT PARQUET)"
                )
            sources.mercury.cache_clear()
            with patch.object(sources, "dataset_files", return_value=[path]):
                self.assertEqual(sources.mercury(), {"sample": ["class Solution: pass"]})
            sources.mercury.cache_clear()
