"""Maximum OR with 2 * 10^4 random values, so ORing the other values afresh for each choice is
quadratic."""

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    return {"nums": [rng.randint(1, 10**9) for _ in range(N)], "k": rng.randint(1, 15)}
