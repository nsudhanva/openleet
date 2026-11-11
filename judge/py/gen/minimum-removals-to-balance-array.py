"""Minimum Removals to Balance Array at n = 2 * 10^4 random values with k up to 10, so trying each
value as the kept minimum and counting the values within k times it is quadratic against
sorting and two pointers."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9
K = 10


def generate(rng):
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)], "k": rng.randint(2, K)}
