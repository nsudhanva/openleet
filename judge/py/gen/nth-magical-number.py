"""Nth Magical Number with n up to 10^9 and a, b up to 4 * 10^4, so counting magical numbers
one by one is hopeless; one seed has a dividing b."""

SEEDS = 3


def generate(rng):
    n = rng.choice((10**9, rng.randint(1, 10**9)))
    a = rng.randint(2, 4 * 10**4)
    b = rng.choice((rng.randint(2, 4 * 10**4), a * rng.randint(1, (4 * 10**4) // a)))
    return {"n": n, "a": a, "b": b}
