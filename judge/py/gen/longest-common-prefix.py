"""Longest Common Prefix with 200 strings of length up to 200 sharing a long prefix (or all
identical), the shortest one placed last."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    prefix = random_string(rng, "ab", rng.randint(150, 200))
    strs = []
    for _ in range(199):
        tail = random_string(rng, ascii_lowercase, 200 - len(prefix))
        strs.append(prefix + tail)
    strs.append(prefix[: rng.randint(len(prefix) - 10, len(prefix))])
    return {"strs": strs}
