"""Most Stones Removed with 1000 unique stones: packed onto few rows and columns (dense
components) or spread so most are isolated."""

SEEDS = 3
N = 1000
TOP = 10**4


def generate(rng):
    width = rng.choice((40, 300, TOP + 1))
    xs = rng.sample(range(TOP + 1), width)
    ys = rng.sample(range(TOP + 1), width)
    cells = rng.sample(range(width * width), N)
    return {"stones": [[xs[c // width], ys[c % width]] for c in cells]}
