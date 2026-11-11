"""One Edit Distance at the maximum 10^4 characters per string, one edit (or two) near the end, so
computing the full edit distance costs 10^8 DP cells."""

from string import ascii_letters, digits

from _shapes import random_string

SEEDS = 2
N = 10**4
ALPHABET = ascii_letters + digits


def generate(rng):
    s = random_string(rng, ALPHABET, N)
    t = list(s)
    edits = 1 if rng.random() < 0.5 else 2
    for _ in range(edits):
        i = rng.randrange(N - 50, len(t))
        kind = rng.randrange(3)
        if kind == 0:
            t[i] = rng.choice([c for c in ALPHABET if c != t[i]])
        elif kind == 1:
            del t[i]
        else:
            t.insert(i, rng.choice(ALPHABET))
    t = "".join(t)[:N]
    return {"s": s, "t": t} if rng.random() < 0.5 else {"s": t, "t": s}
