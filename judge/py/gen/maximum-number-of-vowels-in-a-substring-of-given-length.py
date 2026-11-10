"""Maximum Vowels in a Substring of Length k at length 10^5 with mid-sized k, where recounting
each window is quadratic."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 10**5


def generate(rng):
    alphabet = rng.choice([ascii_lowercase, "aeioubc"])
    s = random_string(rng, alphabet, N)
    return {"s": s, "k": rng.choice([N // 2, rng.randint(1, N)])}
