"""Count Special Integers with n up to 2 * 10^9, far too large to test each number."""

SEEDS = 3


def generate(rng):
    return {"n": rng.choice([2 * 10**9, 1987654320, rng.randint(10**9, 2 * 10**9)])}
