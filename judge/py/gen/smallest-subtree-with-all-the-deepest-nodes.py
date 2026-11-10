"""Smallest Subtree with All Deepest Nodes at 500 nodes with unique values: two long chains of
equal depth (LCA at the root), a single 500-deep chain, or a random tree."""

from _shapes import level_order, pick_shape, random_tree, zigzag_path

SEEDS = 3


def generate(rng):
    shape = pick_shape(rng)
    n = 500
    if shape == 0:
        # Root with two chains of 249 and 250 nodes; the shorter gets one more at the end.
        left, right = [None] * n, [None] * n
        left[0], right[0] = 1, 2
        a, b = 1, 2
        nxt = 3
        while nxt < n:
            left[a] = nxt
            a = nxt
            nxt += 1
            if nxt < n:
                right[b] = nxt
                b = nxt
                nxt += 1
    elif shape == 1:
        left, right = zigzag_path(rng, n)
    else:
        left, right = random_tree(rng, n, swap=False)
    vals = rng.sample(range(0, 501), n)
    return {"root": level_order(vals, left, right)}
