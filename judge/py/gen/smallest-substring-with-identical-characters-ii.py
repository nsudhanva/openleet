"""Smallest Substring With Identical Characters II at n = 5 * 10^4: a random half then one run of
n / 2 equal characters, with numOps 0 or 1, so the answer is ~10^4 and trying every length in
turn with an O(n) check is ~10^4 checks."""

from _shapes import random_string

SEEDS = 2
N = 5 * 10**4


def generate(rng):
    half = N // 2
    s = random_string(rng, "01", half) + rng.choice("01") * (N - half)
    return {"s": s, "numOps": rng.randint(0, 1)}
