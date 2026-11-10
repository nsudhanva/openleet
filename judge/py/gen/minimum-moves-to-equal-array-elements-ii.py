"""Minimum Moves to Equal Array Elements II at n = 10^5 with values near +-10^9 in a window of
4 * 10^4, so the answer fits in 32 bits; trying every target value is quadratic."""

SEEDS = 3
N = 10**5
SPREAD = 4 * 10**4


def generate(rng):
    base = rng.choice((-(10**9), 10**9 - SPREAD, rng.randint(-(10**9), 10**9 - SPREAD)))
    return {"nums": [base + rng.randint(0, SPREAD) for _ in range(N)]}
