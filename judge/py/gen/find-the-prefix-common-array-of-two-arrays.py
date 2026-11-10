"""Prefix Common Array at the maximum n = 50: two random permutations of 1..n."""

SEEDS = 2


def generate(rng):
    a = list(range(1, 51))
    b = list(range(1, 51))
    rng.shuffle(a)
    rng.shuffle(b)
    return {"A": a, "B": b}
