"""Kth Missing Positive with up to 1000 strictly increasing values and k up to 1000, the
answer often past the end of the array."""

SEEDS = 2


def generate(rng):
    size = rng.randint(900, 1000)
    arr = sorted(rng.sample(range(1, 1001), size))
    return {"arr": arr, "k": rng.randint(500, 1000)}
