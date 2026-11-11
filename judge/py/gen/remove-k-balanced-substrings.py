"""Remove K-Balanced Substrings at n = 10^5 as one deep nest of parentheses with k = 1 or 2, so
removing every k-balanced substring pass after pass takes ~n / 2k passes over the string."""

SEEDS = 2
N = 10**5


def generate(rng):
    k = rng.choice((1, 2))
    depth = N // 2 - rng.randrange(3)
    return {"s": "(" * depth + ")" * depth, "k": k}
