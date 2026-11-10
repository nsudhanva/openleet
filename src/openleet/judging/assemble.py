"""Step 3: decide each problem's checker and keep only the tests every reference agrees on.

A reference solution (voter) counts for a problem only if it reproduces every statement
example's official output. A test is kept only if every counting voter ran it and all of them
agree under the problem's checker; the expected output is their shared answer.
"""

import hashlib
import json
import math
from collections.abc import Callable
from typing import Any

import duckdb

from openleet.judging import (
    JUDGE_DIR,
    RESULTS_DIR,
    SPECS_PATH,
    STRESS_DIR,
    TESTS_PATH,
    WORK_DIR,
    WORK_ITEMS_DIR,
    unsupported,
)

FLOAT_TOLERANCE = 1e-5
# Larger exact stress answers are stored as a SHA-256 of their printed form.
DIGEST_MIN_BYTES = 16384
# Strictest first; any-order problems start at "unordered".
CHECKERS = ("exact", "unordered", "unordered_nested")
TEST_KINDS = ("example", "hidden", "stress")

type Matcher = Callable[[Any, Any], bool]


def key(value: Any) -> str:
    """Canonical JSON: equal values give equal text."""
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def normalize(value: Any, checker: str) -> Any:
    """The form two answers must share to be equal under a checker (floats aside)."""
    if checker == "unordered" and isinstance(value, list):
        return sorted(value, key=key)
    if checker == "unordered_nested" and isinstance(value, list):
        inner = [sorted(v, key=key) if isinstance(v, list) else v for v in value]
        return sorted(inner, key=key)
    return value


def close(a: Any, b: Any) -> bool:
    """Equal, with numbers compared to LeetCode's 1e-5 tolerance."""
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return math.isclose(a, b, rel_tol=FLOAT_TOLERANCE, abs_tol=FLOAT_TOLERANCE)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(close(x, y) for x, y in zip(a, b, strict=True))
    return a == b


def matcher(checker: str, floats: bool) -> Matcher:
    def same(a: Any, b: Any) -> bool:
        a, b = normalize(a, checker), normalize(b, checker)
        return close(a, b) if floats else key(a) == key(b)

    return same


def expected_columns(test: dict, entry: dict) -> tuple[str | None, str | None]:
    """A test's `expected` and `expected_sha256` columns: the answer as canonical JSON, or,
    for a big stress answer compared exactly, only the SHA-256 of the line the sandboxed child
    prints for it (judge/py/zygote.py `send`). Equal values print as equal bytes there, so
    the judge compares a submission's raw output bytes against the digest."""
    if test["kind"] == "stress" and entry["checker"] == "exact" and not entry["floats"]:
        printed = json.dumps(test["expected"], separators=(",", ":"), ensure_ascii=False)
        data = printed.encode()
        if len(data) > DIGEST_MIN_BYTES:
            return None, hashlib.sha256(data).hexdigest()
    return key(test["expected"]), None


def has_float(spec: dict) -> bool:
    types = [spec.get("returns", "")] + [m["returns"] for m in spec.get("methods", {}).values()]
    return any("float" in t for t in types)


def answered(result: dict | None) -> bool:
    """A voter's result for one test holds an answer (not an error, timeout or skip)."""
    return result is not None and "out" in result


def agreed(results: list[Any], same: Matcher) -> bool:
    """Every voter answered and all answers match the first."""
    return all(answered(r) for r in results) and all(
        same(results[0]["out"], r["out"]) for r in results[1:]
    )


def stress_tests(slug: str, voters: dict, same: Matcher, cpu: dict) -> list[dict]:
    """Generated stress tests every reference answered alike; adds their CPU time to `cpu`."""
    path = STRESS_DIR / f"{slug}.json"
    if not path.exists():
        return []
    run = json.loads(path.read_text())
    if not set(voters) <= set(run["voters"]):
        return []
    kept = []
    for k, (seed, sha) in enumerate(zip(run["seeds"], run["shas"], strict=True)):
        outs = [run["voters"][name]["results"][k] for name in voters]
        if agreed(outs, same):
            test = {"gen": slug, "seed": seed, "sha": sha}
            kept.append({"kind": "stress", "test": test, "expected": outs[0]["out"]})
    for name in voters:
        cpu[name] += run["voters"][name]["cpuMs"]
    return kept


def judge_problem(item: dict, votes: dict) -> tuple[dict, list[dict]]:
    """The problem's spec entry and its kept tests."""
    examples = item["examples"]
    floats = has_float(item["spec"])
    candidates = (
        CHECKERS[1:] if item["anyOrder"] and item["spec"]["kind"] == "function" else CHECKERS
    )

    def qualified(checker: str) -> dict[str, list]:
        same = matcher(checker, floats)
        return {
            name: v["results"]
            for name, v in votes.items()
            if len(v["results"]) >= len(examples)
            and all(
                answered(r) and same(r["out"], e["output"])
                for r, e in zip(v["results"], examples, strict=False)
            )
        }

    # The checker under which the most references reproduce the examples; ties go stricter.
    by_checker = {c: qualified(c) for c in candidates} if examples else {}
    checker = max(by_checker, key=lambda c: len(by_checker[c]), default=None)
    if checker is None or not by_checker[checker]:
        return unsupported("No reference solution reproduces the examples."), []
    voters, same = by_checker[checker], matcher(checker, floats)

    tests = []
    for i, test in enumerate([*examples, *({"input": x} for x in item["inputs"])]):
        outs = [r[i] for r in voters.values()]
        if agreed(outs, same):
            kind = "example" if i < len(examples) else "hidden"
            expected = test["output"] if kind == "example" else outs[0]["out"]
            tests.append({"kind": kind, "test": {"input": test["input"]}, "expected": expected})
    cpu = {name: votes[name]["cpuMs"] for name in voters}
    tests += stress_tests(item["slug"], voters, same, cpu)
    entry = {
        "supported": True,
        "spec": item["spec"],
        "starter": item["starter"],
        "checker": checker,
        "floats": floats,
        "voters": sorted(voters),
        "refCpuMs": min(cpu.values()),
        # The slowest reference; all of them are accepted, so the limit must admit it.
        "slowCpuMs": max(cpu.values()),
        # Runs custom inputs for the expected answer. Mercury's submissions are used offline
        # only (CC BY-NC), so they are never shipped.
        "reference": next(
            (item["voters"][n] for n in sorted(voters) if not n.startswith("mercury")), None
        ),
    }
    return entry, tests


def assemble() -> None:
    specs: dict[str, dict] = {}
    rows: list[dict] = []
    for path in sorted(WORK_ITEMS_DIR.glob("*.json")):
        item = json.loads(path.read_text())
        slug = item["slug"]
        if not item["supported"]:
            specs[slug] = unsupported(item["reason"])
            continue
        result = RESULTS_DIR / f"{slug}.json"
        if not result.exists():
            specs[slug] = unsupported("Not built yet.")
            continue
        entry, tests = judge_problem(item, json.loads(result.read_text())["voters"])
        specs[slug] = entry
        for i, test in enumerate(tests):
            expected, digest = expected_columns(test, entry)
            rows.append(
                {
                    "slug": slug,
                    "idx": i,
                    "kind": test["kind"],
                    "test": key(test["test"]),
                    "expected": expected,
                    "expected_sha256": digest,
                }
            )
        if entry["supported"]:
            entry["tests"] = {kind: sum(t["kind"] == kind for t in tests) for kind in TEST_KINDS}

    JUDGE_DIR.mkdir(parents=True, exist_ok=True)
    SPECS_PATH.write_text(json.dumps(specs, indent=1, sort_keys=True) + "\n")
    staging = WORK_DIR / "tests.jsonl"
    with staging.open("w") as out:
        out.writelines(key(row) + "\n" for row in rows)
    TESTS_PATH.unlink(missing_ok=True)
    # Sorted by slug so the server's lookups skip all row groups but one; DuckDB's own
    # compression (dictionary, FSST) keeps the corpus small.
    with duckdb.connect(str(TESTS_PATH)) as con:
        con.execute(
            f"""CREATE TABLE tests AS
            FROM read_json('{staging}', columns = {{slug: 'VARCHAR', idx: 'USMALLINT',
                kind: 'VARCHAR', test: 'VARCHAR', expected: 'VARCHAR',
                expected_sha256: 'VARCHAR'}})
            ORDER BY slug, idx"""
        )
        con.execute("CHECKPOINT")
    staging.unlink()
    supported = sum(s["supported"] for s in specs.values())
    print(f"{supported}/{len(specs)} problems judged, {len(rows)} tests -> {TESTS_PATH}")
