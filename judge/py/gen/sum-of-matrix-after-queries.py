"""Sum of Matrix After Queries at n = 10^4 with 2 * 10^4 queries, most on rows and columns not
yet overwritten, so recounting the untouched lines for each query is ~2 * 10^8 steps."""

SEEDS = 2
N = 10**4
Q = 2 * 10**4


def generate(rng):
    queries = []
    for _ in range(Q):
        queries.append([rng.randint(0, 1), rng.randrange(N), rng.randint(0, 10**5)])
    return {"n": N, "queries": queries}
