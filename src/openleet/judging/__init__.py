"""Builds the judge's test data: problem signatures, test inputs and verified expected outputs.

Pipeline (`uv run openleet judge all`):
  prepare   parse sources into one work item per problem (no code runs on the host)
  vote      run every reference solution on every input inside a network-less container
  assemble  keep the tests all references agree on, pick each problem's checker, and write
            data/judge/specs.json and data/judge/tests.duckdb
  stress    run the stress generators (judge/py/gen) and the qualified references on them
  final     assemble again, now with the stress tests

`judge publish` uploads tests.duckdb as a GitHub release asset (it is too big for git) and
records it in data/judge/corpus.json; `judge fetch` downloads and verifies that asset.

Inputs come from LeetCodeDataset (Apache-2.0) and the statements' own examples; expected
outputs are never copied from a dataset, only computed by running independent reference
solutions (LeetCodeDataset's canonical solution, every doocs/leetcode Python solution, and,
where available, accepted LeetCode submissions from Mercury, CC BY-NC 4.0, used offline only).
A test is kept only when all of them agree, and every statement example must match the
statement's own output.
"""

from pathlib import Path

from openleet.data import CACHE_DIR, DATA_DIR

DATASET_DIR = CACHE_DIR / "datasets"
WORK_DIR = CACHE_DIR / "judge"
# One JSON file per problem slug in each: prepare's work items, vote's and stress's results.
WORK_ITEMS_DIR = WORK_DIR / "work"
RESULTS_DIR = WORK_DIR / "results"
STRESS_DIR = WORK_DIR / "stress"
JUDGE_DIR = DATA_DIR / "judge"
SPECS_PATH = JUDGE_DIR / "specs.json"
TESTS_PATH = JUDGE_DIR / "tests.duckdb"
HARNESS_DIR = Path("judge/py")


def unsupported(reason: str) -> dict:
    """The spec entry of a problem the judge cannot run."""
    return {"supported": False, "reason": reason}
