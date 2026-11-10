"""Downloads (once) and reads the sources: LeetCodeDataset, Mercury, doocs Python solutions."""

import json
import re
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

import duckdb

from openleet.data import cached_download, doocs_readme_path
from openleet.judging import DATASET_DIR

HF = "https://huggingface.co/datasets"
LEETCODE_DATASET = {
    "lcd-train.jsonl": f"{HF}/newfacade/LeetCodeDataset/resolve/main/LeetCodeDataset-train.jsonl",
    "lcd-test.jsonl": f"{HF}/newfacade/LeetCodeDataset/resolve/main/LeetCodeDataset-test.jsonl",
}
MERCURY = {
    "mercury-train.parquet": f"{HF}/Elfsong/Mercury/resolve/main/data/train-00000-of-00001.parquet",
    "mercury-eval.parquet": f"{HF}/Elfsong/Mercury/resolve/main/data/eval-00000-of-00001.parquet",
}
PYTHON_BLOCK = re.compile(r"#### Python3\s*\n```python\n(.*?)\n```", re.S)


@dataclass
class Sources:
    """Everything known about one problem's code before anything runs."""

    starter: str | None = None
    entry_point: str | None = None
    # Test inputs as Python source of `candidate(...)` calls (LeetCodeDataset's check function).
    dataset_test: str | None = None
    voters: dict[str, str] = field(default_factory=dict)


def dataset_files(files: dict[str, str]) -> list[Path]:
    """Local copies of a dataset's files (local name -> URL), downloaded on first use."""
    return [cached_download(url, DATASET_DIR / name) for name, url in files.items()]


@cache
def leetcode_dataset() -> dict[str, dict]:
    """LeetCodeDataset rows by slug."""
    rows = {}
    for path in dataset_files(LEETCODE_DATASET):
        with path.open() as lines:
            for line in lines:
                row = json.loads(line)
                rows[row["task_id"]] = row
    return rows


@cache
def mercury() -> dict[str, list[str]]:
    """Accepted LeetCode submissions per slug: the fastest, median and slowest."""
    paths = [str(path) for path in dataset_files(MERCURY)]
    with duckdb.connect() as con:
        query = f"SELECT slug_name, solutions FROM read_parquet({paths!r})"
        rows = con.execute(query).fetchall()
    out: dict[str, list[str]] = {}
    for slug, solutions in rows:
        ranked = sorted(solutions, key=lambda s: int(re.sub(r"\D", "", s["runtime"]) or 0))
        # Spread across the runtime range, so the voters are less alike.
        picks = {0, len(ranked) // 2, len(ranked) - 1} if ranked else set()
        out[slug] = [ranked[i]["solution"] for i in sorted(picks)]
    return out


def doocs_solutions(problem_id: int) -> list[str]:
    path = doocs_readme_path(problem_id)
    return PYTHON_BLOCK.findall(path.read_text()) if path.exists() else []


def sources_for(problem_id: int, slug: str) -> Sources:
    found = Sources()
    if row := leetcode_dataset().get(slug):
        found.starter = row["starter_code"]
        found.entry_point = row["entry_point"]
        found.dataset_test = row["test"]
        found.voters["dataset"] = row["completion"]
    for i, code in enumerate(doocs_solutions(problem_id), 1):
        found.voters[f"doocs{i}"] = code
    for i, code in enumerate(mercury().get(slug, []), 1):
        found.voters[f"mercury{i}"] = code
    return found
