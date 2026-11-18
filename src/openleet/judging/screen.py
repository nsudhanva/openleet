"""Every test must be an input the problem's statement allows. LeetCodeDataset's inputs are
generated, and some break the statement's constraints (a grid with two repeated values where
the problem promises one); the references then agree on an answer to a question the problem
never asks, and a correct solution fails.

judge/py/constraints/<slug>.py states a problem's constraints as code: `check(**input)`
takes a test's input (the keyword arguments of the solution's method, or `ops` and `args` for
a design problem) and asserts each constraint, with a message naming it.

`uv run openleet judge check SLUG...` reports the tests each problem's constraints reject.
`uv run openleet judge screen` drops them from data/judge/tests.duckdb and updates the test
counts in specs.json. It refuses a constraints file that rejects one of the statement's own
examples, since the file is wrong then, not the example.
"""

import importlib.util
import json
import signal
import sys
from collections.abc import Iterator
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from random import Random
from types import ModuleType
from typing import Any

import duckdb

from openleet.judging import HARNESS_DIR, SPECS_PATH, TESTS_PATH, WORK_DIR
from openleet.judging.testdb import TEST_KINDS, write_jsonl

CONSTRAINTS_DIR = HARNESS_DIR / "constraints"
GEN_DIR = HARNESS_DIR / "gen"
# A check runs in linear time; one that takes longer is a bug in the check.
CHECK_SECONDS = 20
PREVIEW_CHARS = 160
# Rejected tests `judge check` lists per problem.
SHOWN = 12


@dataclass(frozen=True)
class Rejected:
    idx: int
    kind: str
    reason: str
    # The check raised something other than AssertionError: likely a bug in the check.
    error: bool
    preview: str


@cache
def loaded(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise FileNotFoundError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def constraints(slug: str) -> ModuleType | None:
    path = CONSTRAINTS_DIR / f"{slug}.py"
    return loaded(path, f"constraints_{slug}") if path.exists() else None


def test_input(test_case: dict) -> dict:
    """A test's input: stored, or made by its stress generator exactly as the judge makes it."""
    if "gen" not in test_case:
        return test_case["input"]
    if str(GEN_DIR) not in sys.path:
        sys.path.append(str(GEN_DIR))  # generators import _shapes
    gen = loaded(GEN_DIR / f"{test_case['gen']}.py", f"gen_{test_case['gen']}")
    return gen.generate(Random(test_case["seed"]))


def _timeout(_signum: int, _frame: Any) -> None:
    raise TimeoutError(f"the check took over {CHECK_SECONDS} s")


def violation(module: ModuleType, data: dict) -> tuple[str, bool] | None:
    """Why the input breaks the constraints and whether the check itself failed, or None."""
    previous = signal.signal(signal.SIGALRM, _timeout)
    signal.alarm(CHECK_SECONDS)
    try:
        module.check(**data)
    except AssertionError as error:
        return str(error) or "a constraint", False
    except Exception as error:
        return f"{type(error).__name__}: {error}", True
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, previous)
    return None


def rows(slugs: list[str] | None = None) -> Iterator[tuple[str, int, str, str]]:
    """(slug, idx, kind, test_case) of the corpus, in order."""
    where = "WHERE slug IN (SELECT unnest(?))" if slugs else ""
    query = f"SELECT slug, idx, kind::VARCHAR, test_case::VARCHAR FROM tests {where} ORDER BY 1, 2"
    with duckdb.connect(str(TESTS_PATH), read_only=True) as con:
        yield from con.execute(query, [slugs] if slugs else []).fetchall()


def rejected(slug: str, tests: list[tuple[int, str, str]]) -> list[Rejected]:
    """The problem's tests its constraints reject (none without a constraints file)."""
    module = constraints(slug)
    if module is None:
        return []
    out = []
    for idx, kind, test_case in tests:
        data = test_input(json.loads(test_case))
        if found := violation(module, data):
            reason, error = found
            preview = json.dumps(data, separators=(",", ":"))[:PREVIEW_CHARS]
            out.append(Rejected(idx, kind, reason, error, preview))
    return out


def by_slug(slugs: list[str] | None = None) -> dict[str, list[tuple[int, str, str]]]:
    grouped: dict[str, list[tuple[int, str, str]]] = {}
    for slug, idx, kind, test_case in rows(slugs):
        grouped.setdefault(slug, []).append((idx, kind, test_case))
    return grouped


def _rejected(item: tuple[str, list[tuple[int, str, str]]]) -> tuple[str, list[Rejected]]:
    return item[0], rejected(*item)


def screen_all(slugs: list[str] | None = None) -> tuple[dict, dict[str, list[Rejected]]]:
    """Each problem's tests and the ones its constraints reject, checked in parallel."""
    grouped = by_slug(slugs)
    with_constraints = {s: t for s, t in grouped.items() if (CONSTRAINTS_DIR / f"{s}.py").exists()}
    with ProcessPoolExecutor() as pool:
        found = dict(pool.map(_rejected, with_constraints.items(), chunksize=8))
    return grouped, found


def check(slugs: list[str]) -> None:
    """`judge check SLUG...`: each problem's rejected tests, for writing its constraints."""
    if not slugs:
        raise SystemExit("usage: openleet judge check SLUG...")
    grouped, found = screen_all(slugs)
    for slug in slugs:
        tests = grouped.get(slug, [])
        if not (CONSTRAINTS_DIR / f"{slug}.py").exists():
            print(f"{slug}: no {CONSTRAINTS_DIR.name}/{slug}.py yet ({len(tests)} tests)")
            continue
        bad = found.get(slug, [])
        examples = sum(r.kind == "example" for r in bad)
        verdict = "EXAMPLE REJECTED, fix the check" if examples else "ok"
        print(f"{slug}: {len(tests)} tests, {len(bad)} rejected; examples {verdict}")
        # The examples and the check's own failures first: those are what need fixing.
        for r in sorted(bad, key=lambda r: (r.kind != "example", not r.error))[:SHOWN]:
            flag = " [check raised]" if r.error else ""
            print(f"  #{r.idx} {r.kind}{flag}: {r.reason} | {r.preview}")
        if len(bad) > SHOWN:
            print(f"  ... {len(bad) - SHOWN} more")


def screen() -> None:
    """`judge screen`: drops the tests the problems' constraints reject from the corpus."""
    grouped, found = screen_all()
    wrong = sorted(s for s, bad in found.items() if any(r.kind == "example" for r in bad))
    if wrong:
        raise SystemExit(
            f"These constraints reject a statement example, fix them first: {', '.join(wrong)}"
        )
    specs = json.loads(SPECS_PATH.read_text())
    dropped = {s: {r.idx for r in bad} for s, bad in found.items() if bad}
    staging = WORK_DIR / "screened.jsonl"
    staging.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(TESTS_PATH), read_only=True) as con:
        all_rows = con.execute(
            "SELECT slug, idx, kind::VARCHAR, test_case::VARCHAR, expected::VARCHAR,"
            " expected_sha256 FROM tests ORDER BY 1, 2"
        ).fetchall()
    with staging.open("w") as out:
        idx_of: dict[str, int] = {}
        counts: dict[str, dict[str, int]] = {}
        for slug, idx, kind, test_case, expected, digest in all_rows:
            if idx in dropped.get(slug, ()):
                continue
            new = idx_of[slug] = idx_of.get(slug, -1) + 1
            counts.setdefault(slug, dict.fromkeys(TEST_KINDS, 0))[kind] += 1
            row = {
                "slug": slug,
                "idx": new,
                "kind": kind,
                "test_case": test_case,
                "expected": expected,
                "expected_sha256": digest,
            }
            out.write(json.dumps(row, separators=(",", ":")) + "\n")
    for slug, entry in specs.items():
        if entry.get("supported") and slug in counts:
            entry["tests"] = counts[slug]
    write_jsonl(TESTS_PATH, staging, "openleet judge screen")
    staging.unlink()
    SPECS_PATH.write_text(json.dumps(specs, indent=1, sort_keys=True) + "\n")
    total = sum(map(len, dropped.values()))
    stress = sum(r.kind == "stress" for bad in found.values() for r in bad)
    print(
        f"{len(found)}/{len(grouped)} problems have constraints; dropped {total} tests from "
        f"{len(dropped)} problems ({stress} stress) -> {TESTS_PATH}"
    )
    for slug in sorted(dropped):
        print(f"  {slug}: {len(dropped[slug])}")
