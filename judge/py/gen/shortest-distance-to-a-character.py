"""Shortest Distance to a Character on 10^4 letters: c only at one end, or c filling the first
~27% and absent after, so scanning outward from each index, or over every occurrence of c,
costs ~2 * 10^7 to 5 * 10^7 steps."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    c = rng.choice(ascii_lowercase)
    others = [x for x in ascii_lowercase if x != c]
    s = [rng.choice(others) for _ in range(N)]
    if shape == 0:
        s[0] = c
    elif shape == 1:
        s[-1] = c
    else:
        # About where both scans cost the same: (N - run)^2 / 2 == N * run.
        run = rng.randint(2600, 2800)
        s[:run] = [c] * run
    return {"s": "".join(s), "c": c}
