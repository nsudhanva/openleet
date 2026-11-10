"""Largest Component by Common Factor with 2 * 10^4 distinct values up to 10^5: random values,
or even numbers that all join one giant component (quadratic gcd checks time out)."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**5


def generate(rng):
    if rng.random() < 0.5:
        nums = rng.sample(range(1, LIMIT + 1), N)
    else:
        nums = rng.sample(range(2, LIMIT + 1, 2), N)
    return {"nums": nums}
