"""Reduction Operations to Make the Array Elements Equal at n = 10^4 with ~9000 distinct values,
so counting the smaller distinct values of each element costs ~10^8 steps."""

SEEDS = 2
N = 10**4
LIMIT = 5 * 10**4


def generate(rng):
    return {"nums": [rng.randint(1, LIMIT) for _ in range(N)]}
