"""Unique Substrings in Wraparound String at n = 10^5: the alphabet cycled over and over (runs
of length 10^5, where enumerating substrings explodes) or random letters."""

from _shapes import pick_shape

SEEDS = 3
N = 10**5
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        start = rng.randrange(26)
        s = "".join(LETTERS[(start + i) % 26] for i in range(N))
    elif shape == 1:
        # Long consecutive runs broken at random points.
        out = []
        cur = rng.randrange(26)
        for _ in range(N):
            cur = (cur + 1) % 26 if rng.random() < 0.97 else rng.randrange(26)
            out.append(LETTERS[cur])
        s = "".join(out)
    else:
        s = "".join(rng.choice(LETTERS) for _ in range(N))
    return {"s": s}
