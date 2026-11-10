"""Maximal Rectangle on a 200 x 200 binary matrix: mostly ones with sparse zeros (large
rectangles, cubic scans time out), or random cells."""

SEEDS = 2
N = 200


def generate(rng):
    p = rng.choice([0.98, 0.6])
    return {"matrix": [["1" if rng.random() < p else "0" for _ in range(N)] for _ in range(N)]}
