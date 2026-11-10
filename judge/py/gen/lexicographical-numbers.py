"""Lexicographical Numbers at n near 5 * 10^4."""

SEEDS = 2


def generate(rng):
    return {"n": rng.choice([5 * 10**4, rng.randint(4 * 10**4, 5 * 10**4)])}
