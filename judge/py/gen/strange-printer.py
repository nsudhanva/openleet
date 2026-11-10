"""Strange Printer at length 100 (O(n^3) interval DP): random over a few letters, or an
alternating pattern that defeats greedy merges."""

from string import ascii_lowercase

from _shapes import pick_shape, random_string

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        s = random_string(rng, "abc", 100)
    elif shape == 1:
        s = random_string(rng, ascii_lowercase, 100)
    else:
        s = ("ab" * 50) if rng.random() < 0.5 else ("abcba" * 20)
    return {"s": s}
