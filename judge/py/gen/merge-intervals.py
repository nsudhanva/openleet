"""Merge Intervals at n = 10^4 over [0, 10^4]: short random intervals, or nested and
chained ones that all merge into a few."""

SEEDS = 3
N = 10**4
TOP = 10**4


def generate(rng):
    span = rng.choice((5, 100, TOP))
    intervals = []
    for _ in range(N):
        a = rng.randint(0, TOP)
        intervals.append([a, rng.randint(a, min(TOP, a + span))])
    return {"intervals": intervals}
