"""Downloads (once) and reads the sources: LeetCodeDataset, Mercury, doocs Python solutions."""

import json
import re
import urllib.request
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

from google.judging import CACHE_DIR, DATASET_DIR

HF = "https://huggingface.co/datasets"
DATASET_FILES = {
    "lcd-train.jsonl": f"{HF}/newfacade/LeetCodeDataset/resolve/main/LeetCodeDataset-train.jsonl",
    "lcd-test.jsonl": f"{HF}/newfacade/LeetCodeDataset/resolve/main/LeetCodeDataset-test.jsonl",
    "mercury-train.parquet": f"{HF}/Elfsong/Mercury/resolve/main/data/train-00000-of-00001.parquet",
    "mercury-eval.parquet": f"{HF}/Elfsong/Mercury/resolve/main/data/eval-00000-of-00001.parquet",
}
# Accepted submissions taken from Mercury per problem, as extra voters.
MERCURY_VOTERS = 3
PYTHON_BLOCK = re.compile(r"#### Python3\s*\n```python\n(.*?)\n```", re.S)


@dataclass
class Sources:
    """Everything known about one problem's code before anything runs."""

    starter: str | None = None
    entry_point: str | None = None
    # Test inputs as Python source of `candidate(...)` calls (LeetCodeDataset's check function).
    dataset_test: str | None = None
    voters: dict[str, str] = field(default_factory=dict)


def download(name: str) -> Path:
    path = DATASET_DIR / name
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(".part")
        urllib.request.urlretrieve(DATASET_FILES[name], tmp)
        tmp.rename(path)
    return path


@cache
def leetcode_dataset() -> dict[str, dict]:
    rows = {}
    for name in ("lcd-train.jsonl", "lcd-test.jsonl"):
        with download(name).open() as lines:
            for line in lines:
                row = json.loads(line)
                rows[row["task_id"]] = row
    return rows


@cache
def mercury() -> dict[str, list[str]]:
    """Accepted LeetCode submissions per slug, fastest first."""
    import duckdb

    paths = [str(download(n)) for n in ("mercury-train.parquet", "mercury-eval.parquet")]
    rows = duckdb.sql(f"SELECT slug_name, solutions FROM read_parquet({paths!r})").fetchall()
    out: dict[str, list[str]] = {}
    for slug, solutions in rows:
        ranked = sorted(solutions, key=lambda s: int(re.sub(r"\D", "", s["runtime"]) or 0))
        # Spread the picks across the runtime range: fastest, median, slowest.
        picks = {0, len(ranked) // 2, len(ranked) - 1} if ranked else set()
        out[slug] = [ranked[i]["solution"] for i in sorted(picks)][:MERCURY_VOTERS]
    return out


def doocs_solutions(problem_id: int) -> list[str]:
    path = CACHE_DIR / "doocs" / f"{problem_id:04d}.md"
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
