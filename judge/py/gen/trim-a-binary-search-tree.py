"""Trim a BST at the maximum 10^4 nodes as one long path (ascending, descending or zigzag) with
about a third of the nodes cut from its deep end and a few from the other, so rebuilding the kept
nodes by repeated BST insertion, or deleting each cut node by a search from the root, is
quadratic."""

from _shapes import insert_bst, level_order, pick_shape

SEEDS = 3
N = 10**4
TOP = 10**4


def generate(rng):
    shape = pick_shape(rng)
    values = sorted(rng.sample(range(TOP + 1), N))
    if shape == 0:
        order = list(range(N))
    elif shape == 1:
        order = list(range(N - 1, -1, -1))
    else:
        # Smallest, largest, second smallest, ...: a path that turns at every node.
        order = [i // 2 if i % 2 == 0 else N - 1 - i // 2 for i in range(N)]
    left, right = insert_bst(values, order)
    deep, shallow = rng.randint(N * 3 // 10, N * 9 // 25), rng.randint(0, N // 100)
    # The ascending path and the zigzag end deep among the large values, the descending one
    # among the small values.
    cut_low, cut_high = (deep, shallow) if shape == 1 else (shallow, deep)
    low, high = values[cut_low], values[N - 1 - cut_high]
    return {"root": level_order(values, left, right, order[0]), "low": low, "high": high}
