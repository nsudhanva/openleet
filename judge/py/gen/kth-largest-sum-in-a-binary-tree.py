"""Kth Largest Sum in a Binary Tree at n = 10^4 nodes shaped as a chain or a deep skewed tree,
so summing each level with its own depth-limited walk from the root costs ~5 * 10^7 visits."""

from _shapes import level_order, pick_shape, shaped_tree, skewed_tree

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        left, right = shaped_tree(rng, N, "chain")
    else:
        left, right = skewed_tree(rng, N, rate=shape * 2)
    vals = [rng.randint(1, 10**6) for _ in range(N)]
    depth, stack = 0, [(0, 1)]
    while stack:
        node, d = stack.pop()
        depth = max(depth, d)
        stack += [(c, d + 1) for c in (left[node], right[node]) if c is not None]
    return {"root": level_order(vals, left, right), "k": rng.randint(depth // 2, depth)}
