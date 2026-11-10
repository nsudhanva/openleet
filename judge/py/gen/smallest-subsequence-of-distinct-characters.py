"""Smallest Subsequence of Distinct Characters on 1000 letters, all 26 present, often in
descending runs that force many stack pops."""

from _shapes import pick_shape

SEEDS = 3
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        s = [rng.choice(LETTERS) for _ in range(1000)]
    elif shape == 1:
        s = list((LETTERS[::-1] * 40)[:1000])
    else:
        s = [rng.choice("abc") for _ in range(1000)]
    return {"s": "".join(s)}
