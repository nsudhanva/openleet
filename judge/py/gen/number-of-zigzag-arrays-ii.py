"""ZigZag Arrays II with n near 10^9 and the widest value range, so only matrix exponentiation
finishes."""

SEEDS = 2


def generate(rng):
    n = rng.randint(9 * 10**8, 10**9)
    lo = rng.randint(1, 3)
    r = rng.randint(72, 75)
    return {"n": n, "l": lo, "r": r}
