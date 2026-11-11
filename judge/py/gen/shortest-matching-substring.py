"""Shortest Matching Substring with s of length 10^5 where the first two parts of p match almost
everywhere and the last part only at the very end, so trying each start and scanning forward for
the remaining parts is O(n^2)."""

from _shapes import pick_shape, random_string

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        s, p = random_string(rng, "aby", N - 2) + "yz", "a*b*yz"
    elif shape == 1:
        s, p = random_string(rng, "ab", N - 2) + "zy", "*ab*zy"
    else:
        s, p = "a" * (N - 1) + "b", "aa*a*ab"
    return {"s": s, "p": p}
