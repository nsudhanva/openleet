"""Zigzag Conversion at the maximum 1000 characters with numRows of 1, 2, near n, or above n."""

from _shapes import pick_shape

SEEDS = 3
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ,."


def generate(rng):
    shape = pick_shape(rng)
    s = "".join(rng.choice(CHARS) for _ in range(1000))
    rows = [rng.choice([1, 2]), rng.randint(3, 50), rng.randint(500, 1000)][shape]
    return {"s": s, "numRows": rows}
