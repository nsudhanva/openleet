"""Find Words Containing Character at the maximum 50 words of 50 letters."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2


def generate(rng):
    alpha = ascii_lowercase[: rng.choice([3, 26])]
    words = [random_string(rng, alpha, rng.randint(1, 50)) for _ in range(50)]
    return {"words": words, "x": rng.choice(alpha)}
