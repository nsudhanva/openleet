"""Scramble String at length 30 over a tiny alphabet: a genuine random scramble (true), or an
anagram of s1 that defeats character-count pruning, so unmemoized recursion explodes."""

from _shapes import random_string

SEEDS = 3


def scramble(rng, s):
    if len(s) <= 1:
        return s
    i = rng.randint(1, len(s) - 1)
    x, y = scramble(rng, s[:i]), scramble(rng, s[i:])
    return y + x if rng.random() < 0.5 else x + y


def generate(rng):
    alphabet = rng.choice(["ab", "abc", "a"])
    s1 = random_string(rng, alphabet, 30)
    if rng.random() < 0.5:
        s2 = scramble(rng, s1)
    else:
        chars = list(s1)
        rng.shuffle(chars)
        s2 = "".join(chars)
    return {"s1": s1, "s2": s2}
