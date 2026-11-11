"""Palindrome Removal at the maximum 100 values drawn from 3 or 20 distinct numbers, so a search
over the arrays left after each removal explodes where the interval DP does ~1.7 * 10^5 steps."""

SEEDS = 2
N = 100


def generate(rng):
    top = rng.choice([3, 20])
    return {"arr": [rng.randint(1, top) for _ in range(N)]}
