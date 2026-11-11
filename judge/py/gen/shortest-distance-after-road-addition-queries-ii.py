"""Shortest Distance After Road Addition Queries II at n = 10^4 with ~8000 short aligned (so never
crossing) roads, which keep the path thousands of cities long, so a BFS after every query is
~10^4 work each."""

SEEDS = 2
N = 10**4
Q = 8000


def generate(rng):
    top = rng.choice([3, 4])
    roads = [
        [a << k, (a + 1) << k]
        for k in range(1, top + 1)
        for a in range(N >> k)
        if (a + 1) << k <= N - 1
    ]
    queries = rng.sample(roads, min(Q, len(roads)))
    return {"n": N, "queries": queries}
