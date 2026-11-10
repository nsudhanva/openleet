"""Minimum Moves to Make Array Complementary at n = 10^5 with limit up to 10^5; trying every
target sum against every pair is 2 * 10^10 steps."""

SEEDS = 3
N = 10**5


def generate(rng):
    limit = rng.choice((10**5, 2, rng.randint(1, 10**5)))
    return {"nums": [rng.randint(1, limit) for _ in range(N)], "limit": limit}
