"""Each problem's time limit, in reference milliseconds (judge/py/calibrate.py): the judge
scales it by how fast its machine runs at the moment, so it holds on any machine and load.

The limit follows the trusted references (LeetCodeDataset's and doocs' solutions, which are
written for the intended complexity), never Mercury's crowd submissions: those keep voting on
answers, but the slowest of them is often a worse complexity class that LeetCode let through.

A submission may take MARGIN times the fastest trusted reference, up to MARGIN_CAP_MS. Accepted
Mercury submissions of the intended complexity written clumsily (memoized recursion, a sorted
container searched by hand, tuples as dict keys) took up to 41 times as long, and 50 leaves
room for measuring noise; the next complexity class does n / log2 n times the work, 180 times
or more on stress inputs of 2,000 elements and up. FLOOR_MS absorbs fixed costs and measuring
noise on the many problems whose references take a few milliseconds; below it, Mercury's slow
submissions were mostly quadratic on tests too small to tell. Every trusted reference passes,
with room for noise (SLOWEST_MARGIN).
"""

import json

import duckdb

from openleet.judging import SPECS_PATH, TESTS_PATH, trusted
from openleet.judging.timing import fingerprint, problem_tests, timings

MARGIN = 50.0
MARGIN_CAP_MS = 10_000
SLOWEST_MARGIN = 2.0
FLOOR_MS = 1000
# The server's cap (server/src/judge.rs, limits::MAX_MS).
CAP_MS = 30_000


def limit_ms(times: list[int]) -> int:
    """The limit for references that took `times` (reference ms)."""
    clumsy = min(MARGIN * min(times), MARGIN_CAP_MS)
    return round(min(CAP_MS, max(FLOOR_MS, clumsy, SLOWEST_MARGIN * max(times))))


def set_limit(entry: dict, measured: dict[str, dict] | None) -> list[str]:
    """Sets `cpuMs` (each trusted reference's time) and `limitMs` on a problem's spec entry,
    from the references' timings through the judge, else from their voting times (the entry's
    `cpuMs`). Returns the trusted references the judge did not accept."""
    if measured is None:
        times = entry.get("cpuMs") or {}
        failed = []
    else:
        times = {n: t["cpuMs"] for n, t in measured.items() if t["verdict"] == "accepted"}
        failed = [n for n, t in measured.items() if trusted(n) and t["verdict"] != "accepted"]
    # Problems without a trusted reference fall back on the crowd's.
    times = {n: ms for n, ms in times.items() if trusted(n)} or times
    if times:
        entry["cpuMs"] = times
        entry["limitMs"] = limit_ms(list(times.values()))
    return failed


def refresh_limits() -> None:
    """Sets every problem's limit in specs.json from the timings cached for its current tests
    (see timing.py), without touching the tests."""
    specs = json.loads(SPECS_PATH.read_text())
    failures = []
    with duckdb.connect(str(TESTS_PATH), read_only=True) as con:
        for slug, entry in sorted(specs.items()):
            if entry["supported"]:
                measured = timings(slug, fingerprint(problem_tests(con, slug)))
                failures += [f"{slug} {name}" for name in set_limit(entry, measured)]
    SPECS_PATH.write_text(json.dumps(specs, indent=1, sort_keys=True) + "\n")
    limits = [e["limitMs"] for e in specs.values() if e.get("limitMs")]
    print(f"{len(limits)} limits set; {sum(ms >= CAP_MS for ms in limits)} at the {CAP_MS} ms cap")
    if failures:
        print(f"{len(failures)} trusted references not accepted by the judge:")
        print("\n".join(f"  {f}" for f in failures))
