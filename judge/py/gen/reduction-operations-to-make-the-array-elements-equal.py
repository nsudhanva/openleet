"""Reduction Operations to Make the Array Elements Equal at n = 5 * 10^4 with ~3 * 10^4 distinct
values, so counting the smaller distinct values of each element costs ~10^9 steps, even as a
C-speed list.index."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 5 * 10**4


def generate(rng):
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)]}
