"""Top K Frequent Words at the maximum 500 words with many frequency ties, so the
lexicographic tie-break decides the answer."""

from _shapes import random_string

SEEDS = 3
N = 500
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    pool = sorted({random_string(rng, LETTERS[:4], rng.randint(1, 10)) for _ in range(150)})
    pool = pool[: rng.randint(20, len(pool))]
    words = [rng.choice(pool) for _ in range(N)]
    unique = len(set(words))
    return {"words": words, "k": rng.randint(1, unique)}
