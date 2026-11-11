"""Find the Number of Distinct Colors Among the Balls with 3 * 10^4 queries on mostly new
balls, so recounting the distinct colors after each query is ~5 * 10^8 steps."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    limit = rng.choice((10**9, N))
    colors = rng.choice((10**9, 1000))
    queries = [[rng.randint(0, limit), rng.randint(1, colors)] for _ in range(N)]
    return {"limit": limit, "queries": queries}
