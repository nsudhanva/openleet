"""Minimum Interval to Include Each Query with 10^5 intervals and 10^5 queries over
[1, 10^7]: wide nested intervals so a per-query scan is 10^10 steps."""

SEEDS = 3
N = 10**5
TOP = 10**7


def generate(rng):
    span = rng.choice((1000, 10**5, TOP))
    intervals = []
    for _ in range(N):
        a = rng.randint(1, TOP)
        intervals.append([a, rng.randint(a, min(TOP, a + span))])
    queries = [rng.randint(1, TOP) for _ in range(N)]
    return {"intervals": intervals, "queries": queries}
