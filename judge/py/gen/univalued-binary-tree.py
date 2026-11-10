"""Univalued Binary Tree at the maximum 100 nodes, all equal or with one different value at
the last level-order position."""

SEEDS = 2
N = 100


def generate(rng):
    differ = rng.random() < 0.5
    val = rng.randrange(100)
    root = [val] * N
    if differ:
        root[-1] = (val + 1) % 100
    return {"root": root}
