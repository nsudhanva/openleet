"""Zigzag Conversion at the maximum 1000 characters with numRows of 1, 2, near n, or above n."""

from string import ascii_letters

from _shapes import pick_shape, random_string

SEEDS = 3
CHARS = ascii_letters + ",."


def generate(rng):
    shape = pick_shape(rng)
    s = random_string(rng, CHARS, 1000)
    rows = [rng.choice([1, 2]), rng.randint(3, 50), rng.randint(500, 1000)][shape]
    return {"s": s, "numRows": rows}
