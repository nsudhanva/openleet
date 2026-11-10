"""Path Existence Queries II at n = 10^5 and 10^5 queries with a small maxDiff, so shortest
paths are thousands of hops long and per-query BFS is far too slow."""

SEEDS = 2
N = 10**5
Q = 10**5


def generate(rng):
    max_diff = rng.choice([3, 50])
    nums = [rng.randint(0, 10**5) for _ in range(N)]
    if rng.random() < 0.5:
        # Punch a hole so some queries are unreachable.
        lo = rng.randint(10**4, 9 * 10**4)
        nums = [x if not lo <= x < lo + max_diff + 1 else lo - 1 for x in nums]
    queries = []
    for _ in range(Q):
        u = rng.randrange(N)
        queries.append([u, u if rng.random() < 0.01 else rng.randrange(N)])
    return {"n": N, "nums": nums, "maxDiff": max_diff, "queries": queries}
