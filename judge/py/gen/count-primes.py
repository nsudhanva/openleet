"""Count Primes with n at or near 5 * 10^6, too large for trial division."""

SEEDS = 3


def generate(rng):
    return {"n": rng.choice([5 * 10**6, 5 * 10**6 - 1, rng.randint(4 * 10**6, 5 * 10**6)])}
