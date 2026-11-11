"""Most Beautiful Item for Each Query at 2 * 10^4 items and 2 * 10^4 queries with random prices
and beauties, so scanning every item for every query is ~4 * 10^8 steps."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    items = [[rng.randint(1, 10**9), rng.randint(1, 10**9)] for _ in range(N)]
    return {"items": items, "queries": [rng.randint(1, 10**9) for _ in range(N)]}
