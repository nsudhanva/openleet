"""Minimized Maximum of Products at n = 10^5 stores with up to 10^5 product types; linear
search over the answer instead of binary search is slow."""

SEEDS = 3
N = 10**5


def generate(rng):
    m = rng.choice((N, 1, rng.randint(1, N)))
    quantities = [rng.randint(1, 10**5) for _ in range(m)]
    return {"n": N, "quantities": quantities}
