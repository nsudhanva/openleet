"""Minimum Cost to Make Array Equalindromic at n = 2 * 10^4 distinct large values, so pricing
the palindromes next to every element with a pass over the array is quadratic."""

SEEDS = 2
N = 2 * 10**4
LIMIT = 10**9


def generate(rng):
    return {"nums": rng.sample(range(1, LIMIT + 1), N)}
