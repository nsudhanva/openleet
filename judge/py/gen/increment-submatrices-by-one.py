"""Increment Submatrices by One at n = 100 with the maximum 10^4 queries, each covering most of
the matrix, so adding cell by cell costs ~5 * 10^7 steps."""

SEEDS = 2
N = 100
QUERIES = 10**4


def generate(rng):
    queries = []
    for _ in range(QUERIES):
        r1, c1 = rng.randrange(N // 4), rng.randrange(N // 4)
        r2, c2 = rng.randrange(N - N // 4, N), rng.randrange(N - N // 4, N)
        queries.append([r1, c1, r2, c2])
    return {"n": N, "queries": queries}
