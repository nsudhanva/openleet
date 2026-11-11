"""Graph Connectivity With Threshold at n = 5000 with a small threshold and 10^4 queries, so
testing every pair of cities for a common divisor does ~1.25 * 10^7 gcds."""

SEEDS = 2
N = 5000
QUERIES = 10**4


def generate(rng):
    threshold = rng.randint(1, 4)
    queries = []
    for _ in range(QUERIES):
        a = rng.randint(1, N)
        b = rng.randint(1, N - 1)
        queries.append([a, b + (b >= a)])
    return {"n": N, "threshold": threshold, "queries": queries}
