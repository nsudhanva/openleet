"""Concatenated Words at 10^4 unique words (total length <= 10^5): words built from a small base
vocabulary so most split many ways, plus long runs of 'a' ending in other letters that defeat
backtracking without memoization."""

from _shapes import random_string

SEEDS = 2
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    words = set()
    total = 0

    def add(w):
        nonlocal total
        if w not in words and 1 <= len(w) <= 30 and total + len(w) <= 10**5 and len(words) < 10**4:
            words.add(w)
            total += len(w)

    for k in range(1, rng.choice([8, 12]) + 1):
        add("a" * k)
    for c in LETTERS[1:]:
        add("a" * 29 + c)
        for d in LETTERS[1:6]:
            add("a" * 28 + c + d)
    alphabet = rng.choice(["abc", "abcdef"])
    base = sorted({random_string(rng, alphabet, rng.randint(2, 5)) for _ in range(300)})
    for w in base:
        add(w)
    while len(words) < 10**4 and total < 10**5 - 30:
        parts = [rng.choice(base) for _ in range(rng.randint(2, 8))]
        w = "".join(parts)[:30]
        if rng.random() < 0.2:
            w = w[:-1] + rng.choice("xyz")
        add(w)
    out = sorted(words)
    rng.shuffle(out)
    return {"words": out}
