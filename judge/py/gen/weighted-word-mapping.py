"""Weighted Word Mapping at the maximum 100 words of 10 letters with weights up to 100."""

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    words = ["".join(rng.choice(LETTERS) for _ in range(rng.randint(1, 10))) for _ in range(100)]
    return {"words": words, "weights": [rng.randint(1, 100) for _ in range(26)]}
