"""Builds the judge's test data: problem signatures, test inputs and verified expected outputs.

Pipeline (`uv run google judge all`):
  prepare   parse sources into one work item per problem (no code runs on the host)
  vote      run every reference solution on every input inside a network-less container
  assemble  keep the tests all references agree on, pick each problem's checker, and write
            data/judge/specs.json and data/judge/tests.duckdb

Inputs come from LeetCodeDataset (Apache-2.0) and the statements' own examples; expected
outputs are never copied from a dataset, only computed by running independent reference
solutions (LeetCodeDataset's canonical solution, every doocs/leetcode Python solution, and,
where available, accepted LeetCode submissions from Mercury, CC BY-NC 4.0, used offline only).
A test is kept only when all of them agree, and every statement example must match the
statement's own output.
"""

from pathlib import Path

DATA_DIR = Path("data")
CACHE_DIR = DATA_DIR / ".cache"
DATASET_DIR = CACHE_DIR / "datasets"
WORK_DIR = CACHE_DIR / "judge"
JUDGE_DIR = DATA_DIR / "judge"
SPECS_PATH = JUDGE_DIR / "specs.json"
TESTS_PATH = JUDGE_DIR / "tests.duckdb"
HARNESS_DIR = Path("judge/py")
