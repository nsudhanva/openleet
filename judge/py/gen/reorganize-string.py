"""Reorganize String at the maximum length 500: one letter at exactly the feasibility limit
(ceil(n/2)), or one more than that so it is impossible."""

from string import ascii_lowercase

SEEDS = 2
N = 500


def generate(rng):
    top = N // 2 + rng.choice([0, 1])
    c = rng.choice(ascii_lowercase)
    rest = [x for x in ascii_lowercase if x != c]
    s = [c] * top + [rng.choice(rest) for _ in range(N - top)]
    rng.shuffle(s)
    return {"s": "".join(s)}
