"""Minimum Operations to Make Binary Array Elements Equal to One II at n = 3 * 10^4 random bits,
so ~1.5 * 10^4 suffix flips are needed and flipping each suffix element by element is
quadratic."""

SEEDS = 2
N = 3 * 10**4


def generate(rng):
    return {"nums": [rng.randrange(2) for _ in range(N)]}
