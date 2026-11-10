"""Reorganize String at the maximum length 500: one letter at exactly the feasibility limit
(ceil(n/2)), or one more than that so it is impossible."""

SEEDS = 2
N = 500
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    top = N // 2 + rng.choice([0, 1])
    c = rng.choice(LETTERS)
    rest = [x for x in LETTERS if x != c]
    s = [c] * top + [rng.choice(rest) for _ in range(N - top)]
    rng.shuffle(s)
    return {"s": "".join(s)}
