"""Super Egg Drop at n = 10^4 floors with many eggs or very few, the sizes where the O(k n^2)
DP is far too slow."""

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    if shape == 0:
        return {"k": 100, "n": 10**4}
    if shape == 1:
        return {"k": rng.randint(2, 4), "n": rng.randint(9000, 10**4)}
    return {"k": rng.randint(5, 100), "n": rng.randint(5000, 10**4)}
