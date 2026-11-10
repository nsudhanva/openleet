"""Unique Substrings in Wraparound String at n = 10^5: the alphabet cycled over and over (runs
of length 10^5, where enumerating substrings explodes) or random letters."""

from string import ascii_lowercase

from _shapes import pick_shape, random_string

SEEDS = 3
N = 10**5


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        start = rng.randrange(26)
        s = "".join(ascii_lowercase[(start + i) % 26] for i in range(N))
    elif shape == 1:
        # Long consecutive runs broken at random points.
        out = []
        cur = rng.randrange(26)
        for _ in range(N):
            cur = (cur + 1) % 26 if rng.random() < 0.97 else rng.randrange(26)
            out.append(ascii_lowercase[cur])
        s = "".join(out)
    else:
        s = random_string(rng, ascii_lowercase, N)
    return {"s": s}
