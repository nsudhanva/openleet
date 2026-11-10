"""Numbers At Most N with n near 10^9 and many digits, so enumerating candidates is far too
slow."""

SEEDS = 2


def generate(rng):
    k = rng.randint(5, 9)
    digits = sorted(rng.sample("123456789", k))
    return {"digits": digits, "n": rng.randint(9 * 10**8, 10**9)}
