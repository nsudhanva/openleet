"""Subdomain Visit Count at the maximum 100 entries sharing a few top-level domains, so
counts must aggregate across many entries."""

from string import ascii_lowercase

from _shapes import random_string

SEEDS = 2
N = 100


def word(rng, lo, hi):
    return random_string(rng, ascii_lowercase, rng.randint(lo, hi))


def generate(rng):
    tops = [word(rng, 2, 4) for _ in range(3)]
    mids = [word(rng, 1, 20) for _ in range(10)]
    out = []
    for _ in range(N):
        parts = [rng.choice(mids), rng.choice(tops)]
        if rng.random() < 0.6:
            parts.insert(0, word(rng, 1, 20))
        out.append(f"{rng.randint(1, 10**4)} {'.'.join(parts)}")
    return {"cpdomains": out}
