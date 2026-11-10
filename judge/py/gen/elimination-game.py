"""Elimination Game with n up to 10^9, too large to simulate the list."""

SEEDS = 3


def generate(rng):
    return {"n": rng.choice([10**9, 2**29, rng.randint(10**8, 10**9)])}
