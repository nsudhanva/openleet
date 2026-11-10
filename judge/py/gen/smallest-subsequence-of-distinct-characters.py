"""Smallest Subsequence of Distinct Characters on 1000 letters, all 26 present, often in
descending runs that force many stack pops."""

from string import ascii_lowercase

from _shapes import pick_shape

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        s = [rng.choice(ascii_lowercase) for _ in range(1000)]
    elif shape == 1:
        s = list((ascii_lowercase[::-1] * 40)[:1000])
    else:
        s = [rng.choice("abc") for _ in range(1000)]
    return {"s": "".join(s)}
