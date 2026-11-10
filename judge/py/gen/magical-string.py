"""Magical String at n near 10^5."""

SEEDS = 2


def generate(rng):
    return {"n": rng.choice([10**5, rng.randint(9 * 10**4, 10**5)])}
