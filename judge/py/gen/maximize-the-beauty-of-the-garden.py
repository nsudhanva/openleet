"""Maximize the Beauty of the Garden at n = 3 * 10^4 flowers of only 3 beauty values, or of 10^4 or
1.5 * 10^4 values with 3 or 2 copies each, so pairing every two equal flowers, or summing between
each value's ends, is >= 1.5 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
N = 3 * 10**4
TOP = 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        pool = rng.sample(range(-TOP, TOP + 1), 3)
        return {"flowers": [rng.choice(pool) for _ in range(N)]}
    copies = 3 if shape == 1 else 2
    flowers = [v for v in rng.sample(range(-TOP, TOP + 1), N // copies) for _ in range(copies)]
    rng.shuffle(flowers)
    return {"flowers": flowers}
