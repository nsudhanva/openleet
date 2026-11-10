"""Shortest Distance to a Character on 10^4 letters where c is rare (sometimes only at one end),
so per-position scans run long."""

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    n = 10**4
    c = rng.choice("abcdefghijklmnopqrstuvwxyz")
    others = [x for x in "abcdefghijklmnopqrstuvwxyz" if x != c]
    s = [rng.choice(others) for _ in range(n)]
    if shape == 0:
        s[0] = c
    elif shape == 1:
        s[-1] = c
    else:
        for i in rng.sample(range(n), 20):
            s[i] = c
    return {"s": "".join(s), "c": c}
