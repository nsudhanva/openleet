"""strStr at 10^4 characters with near-matches everywhere: haystack of 'a's and a needle of
'a's ending in 'b', the quadratic worst case for a naive scan."""

from _shapes import random_string

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.randrange(3)
    if shape == 0:
        m = rng.choice([100, 5000])
        haystack = "a" * (N - 1) + rng.choice("ab")
        needle = "a" * (m - 1) + "b"
    elif shape == 1:
        unit = random_string(rng, "ab", 7)
        haystack = (unit * (N // 7 + 1))[: N - 1] + "c"
        needle = (unit * 800)[:5000] + rng.choice("ac")
    else:
        haystack = random_string(rng, "ab", N)
        start = rng.randrange(N - 3000)
        needle = haystack[start : start + 3000]
    return {"haystack": haystack, "needle": needle}
