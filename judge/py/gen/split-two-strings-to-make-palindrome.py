"""Split Two Strings to Make Palindrome at length 10^5 where a's first half mirrors b's second
half except for a non-palindromic middle (or a and b are random): the answer is false, so
building and checking both strings at every split is ~4 * 10^10 character steps."""

from _shapes import random_string

SEEDS = 2
N = 10**5


def generate(rng):
    if rng.random() < 0.5:
        a, b = random_string(rng, "ab", N), random_string(rng, "ab", N)
    else:
        half = N // 2 - 10
        p = random_string(rng, "ab", half)
        a = p + "abcdefghijklmnopqrst" + random_string(rng, "ab", half)
        b = random_string(rng, "ab", half) + "pqrstuvwxyzabcdefghi" + p[::-1]
        if rng.random() < 0.5:
            a, b = b, a
    return {"a": a, "b": b}
