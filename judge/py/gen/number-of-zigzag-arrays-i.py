"""ZigZag Arrays I near the limits n = 2000 and a value range close to 2000, the worst case for
the O(n * (r - l)) DP."""

SEEDS = 2


def generate(rng):
    n = rng.randint(1900, 2000)
    lo = rng.randint(1, 50)
    r = rng.randint(1900, 2000)
    return {"n": n, "l": lo, "r": r}
