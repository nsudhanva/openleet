"""Largest Value in Each Tree Row with 10^4 nodes over the full 32-bit range on a tree thousands
of levels deep (a zigzag path, a thin tree or a skewed one), so one DFS per row is quadratic."""

from _shapes import level_order, pick_shape, skewed_tree, thin_tree, zigzag_path

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        left, right = zigzag_path(rng, N, -1)
    elif shape == 1:
        left, right = thin_tree(rng, N, 3, -1)
    else:
        left, right = skewed_tree(rng, N, -1)
    vals = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    return {"root": level_order(vals, left, right, empty=-1)}
