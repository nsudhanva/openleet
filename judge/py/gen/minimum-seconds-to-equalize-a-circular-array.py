"""Minimum Seconds to Equalize a Circular Array at n = 2 * 10^4 drawn from 10^4 values, so finding
each value's widest circular gap by a pass over the whole array is ~10^8 steps against one
grouping pass."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    pool = rng.sample(range(1, LIMIT + 1), N // 2)
    return {"nums": [rng.choice(pool) for _ in range(N)]}
