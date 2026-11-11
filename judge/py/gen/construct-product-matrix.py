"""Construct Product Matrix with 3 * 10^4 cells (one row, 100 x 300 or one column), values
coprime to 12345 except one multiple of 3 and one of 5, so no running product hits 0 and
multiplying the other cells for each cell costs 9 * 10^8 steps."""

from _shapes import pick_shape

SEEDS = 3
CELLS = 3 * 10**4
SIDE = 100


def value(rng):
    while True:
        v = rng.randint(1, 10**9)
        if v % 3 and v % 5 and v % 823:
            return v


def multiple(rng, k):
    while True:
        v = k * rng.randint(1, 10**8)
        if v % 823:
            return v


def generate(rng):
    n, m = ((1, CELLS), (SIDE, CELLS // SIDE), (CELLS, 1))[pick_shape(rng)]
    flat = [value(rng) for _ in range(n * m)]
    a, b = rng.sample(range(n * m), 2)
    flat[a] = multiple(rng, 3)
    flat[b] = multiple(rng, 5)
    return {"grid": [flat[i * m : (i + 1) * m] for i in range(n)]}
