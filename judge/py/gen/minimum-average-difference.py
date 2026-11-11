"""Minimum Average Difference at n = 5 * 10^4, so summing both sides afresh at every index is
2.5 * 10^9 additions."""

SEEDS = 2
N = 5 * 10**4
LIMIT = 10**5


def generate(rng):
    return {"nums": [rng.randint(0, LIMIT) for _ in range(N)]}
