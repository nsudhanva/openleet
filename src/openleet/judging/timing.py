"""Step 6 (`judge time`): submits every reference solution to running judge daemons, against
exactly the tests a submission gets, and records each one's verdict and CPU time. The daemon
reports CPU time in reference milliseconds (judge/py/calibrate.py), so the times do not depend
on the machine or how busy it is, and parallel daemons are fine. Each problem's time limit
follows from them (limits.py); results are cached per problem, keyed by the tests they ran on.

Start the daemons first, for example `docker compose --profile dev up -d judge-dev` for one on
tcp://127.0.0.1:7777; JUDGE_SOCKETS takes a comma-separated list of tcp://host:port.
"""

import hashlib
import json
import os
import socket
import threading
from collections.abc import Iterator
from concurrent.futures import ThreadPoolExecutor
from typing import Any

import duckdb

from openleet.judging import SPECS_PATH, TESTS_PATH, TIMING_DIR, WORK_ITEMS_DIR, trusted

DEFAULT_SOCKETS = "tcp://127.0.0.1:7777"
# The judge's own cap: trusted references get all of it, so a slow one is measured, not cut off.
TIMING_LIMIT_MS = 30_000
# Mercury's submissions set no limit; they are timed only far enough to tell how they compare
# (well past any limit): at least this long, and this many times the trusted references.
CROWD_FLOOR_MS = 2000
CROWD_OVER_FASTEST = 50
CROWD_OVER_SLOWEST = 3
# The daemon runs a job at most twice, each within its wall-clock limit, plus calibration.
REPLY_TIMEOUT_S = 600


def problem_tests(con: duckdb.DuckDBPyConnection, slug: str) -> list[tuple[str, str, Any]]:
    """A problem's tests in judging order: (kind, test case JSON, expected) as the server
    sends them, expected being {"value": ...} or {"sha256": ...}."""
    rows = con.execute(
        "SELECT kind::VARCHAR, test_case::VARCHAR, expected::VARCHAR, expected_sha256"
        " FROM tests WHERE slug = ? ORDER BY idx",
        [slug],
    ).fetchall()
    return [
        (kind, case, {"value": json.loads(value)} if digest is None else {"sha256": digest})
        for kind, case, value, digest in rows
    ]


def fingerprint(tests: list[tuple[str, str, Any]]) -> str:
    """Identifies the tests a timing ran on, so a rebuilt corpus is timed again."""
    text = json.dumps([[json.loads(case), want] for _, case, want in tests], sort_keys=True)
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def job(entry: dict, tests: list[tuple[str, str, Any]], code: str, limit_ms: int) -> dict:
    """A submission's job, as the server builds it (server/src/judge.rs `submit`)."""
    return {
        "spec": entry["spec"],
        "code": code,
        "tests": [json.loads(case) for _, case, _ in tests],
        "expected": [want for _, _, want in tests],
        "checker": entry["checker"],
        "floats": entry["floats"],
        "cpu_limit_ms": limit_ms,
        "stop_on_failure": True,
        "capture_stdout": False,
    }


def send(endpoint: str, request: dict) -> dict:
    """One job to a daemon at tcp://host:port, and its outcome."""
    host, port = endpoint.removeprefix("tcp://").rsplit(":", 1)
    with socket.create_connection((host, int(port)), timeout=REPLY_TIMEOUT_S) as conn:
        conn.sendall(json.dumps(request).encode() + b"\n")
        with conn.makefile("rb") as reply:
            return json.loads(reply.readline())


def summary(outcome: dict) -> dict:
    """What the cache keeps of an outcome: the verdict, the CPU time in reference ms, how slow
    the machine was, and each test's own CPU time (for telling input sizes apart)."""
    ends = [c["cpu_ms"] for c in outcome["cases"]]
    return {
        "verdict": outcome["verdict"],
        "cpuMs": outcome["cpu_ms"],
        "slowdown": round(outcome.get("slowdown", 1.0), 3),
        "rerun": outcome.get("rerun", False),
        "failed": outcome["failed"],
        "error": (outcome.get("error") or "")[:300] or None,
        "testMs": [b - a for a, b in zip([0, *ends], ends, strict=False)],
    }


def cached(slug: str, print_: str) -> dict | None:
    """The timing cached for this problem, if it ran on these tests."""
    path = TIMING_DIR / f"{slug}.json"
    if not path.exists():
        return None
    timing = json.loads(path.read_text())
    return timing if timing.get("tests") == print_ else None


def endpoints() -> list[str]:
    sockets = os.environ.get("JUDGE_SOCKETS", DEFAULT_SOCKETS).split(",")
    return [s.strip() for s in sockets if s.strip()]


def todo(specs: dict, con: duckdb.DuckDBPyConnection) -> Iterator[tuple[str, dict, list]]:
    for slug, entry in sorted(specs.items()):
        if entry["supported"]:
            tests = problem_tests(con, slug)
            if tests and cached(slug, fingerprint(tests)) is None:
                yield slug, entry, tests


def time_references() -> None:
    """Times every reference of every problem not timed on its current tests yet."""
    specs = json.loads(SPECS_PATH.read_text())
    TIMING_DIR.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(TESTS_PATH), read_only=True) as con:
        work = list(todo(specs, con))
    sockets = endpoints()
    free = list(sockets)
    lock = threading.Lock()
    print(f"Timing {len(work)} problems on {len(sockets)} judges", flush=True)

    def one(item: tuple[str, dict, list]) -> None:
        slug, entry, tests = item
        codes = json.loads((WORK_ITEMS_DIR / f"{slug}.json").read_text())["voters"]
        with lock:
            endpoint = free.pop()

        def timed(names: list[str], limit_ms: int) -> dict[str, dict]:
            return {
                name: summary(send(endpoint, job(entry, tests, codes[name], limit_ms)))
                for name in names
            }

        try:
            voters = timed([n for n in entry["voters"] if trusted(n)], TIMING_LIMIT_MS)
            times = [v["cpuMs"] for v in voters.values() if v["verdict"] == "accepted"]
            crowd = [n for n in entry["voters"] if not trusted(n)]
            bound = TIMING_LIMIT_MS
            if times:
                wanted = max(CROWD_FLOOR_MS, CROWD_OVER_FASTEST * min(times))
                bound = min(TIMING_LIMIT_MS, max(wanted, CROWD_OVER_SLOWEST * max(times)))
            voters |= timed(crowd, bound)
        finally:
            with lock:
                free.append(endpoint)
        out = {"slug": slug, "tests": fingerprint(tests), "voters": voters}
        (TIMING_DIR / f"{slug}.json").write_text(json.dumps(out))

    done = 0
    with ThreadPoolExecutor(len(sockets)) as pool:
        for _ in pool.map(one, work):
            done += 1
            if done % 100 == 0:
                print(f"  {done}/{len(work)}", flush=True)


def timings(slug: str, tests_print: str) -> dict[str, dict] | None:
    """Each reference's timing on the problem's current tests, if measured."""
    timing = cached(slug, tests_print)
    return None if timing is None else timing["voters"]


def tests_print_of(rows: list[dict]) -> str:
    """`fingerprint` of a problem's tests as assemble holds them (its test rows)."""
    return fingerprint(
        [
            (
                r["kind"],
                r["test_case"],
                {"value": json.loads(r["expected"])}
                if r["expected_sha256"] is None
                else {"sha256": r["expected_sha256"]},
            )
            for r in rows
        ]
    )
