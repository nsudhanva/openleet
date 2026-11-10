"""Palindrome Pairs with 5000 unique words over a tiny alphabet, many of them reverses or
palindromic extensions of each other, so pairs are plentiful and checking all n^2 pairs is
too slow."""

from _shapes import random_string

SEEDS = 2
N = 5000


def generate(rng):
    maxlen = rng.choice([12, 40])
    alpha = "ab" if rng.random() < 0.5 else "abc"
    words = set()
    order = []

    def add(w):
        if w not in words:
            words.add(w)
            order.append(w)

    add("")
    while len(order) < N:
        w = random_string(rng, alpha, rng.randint(3, maxlen))
        add(w)
        roll = rng.random()
        if roll < 0.3 and len(order) < N:
            add(w[::-1])
        elif roll < 0.5 and len(order) < N:
            # A word plus the reverse of its prefix (palindromic suffix trick).
            k = rng.randint(1, len(w))
            add(w[:k][::-1])
    rng.shuffle(order)
    return {"words": order}
