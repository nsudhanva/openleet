"""Binary Tree Longest Consecutive Sequence: a 10^4-node zigzag chain or thin tree whose values
rise by one per level, or a 3 * 10^4-node comb (a rising spine with a leaf off every node), so
walking down from every node, or rescanning every root-to-leaf path, is ~5 * 10^7 steps or more."""

from _shapes import level_order, pick_shape, thin_tree, zigzag_path

SEEDS = 3
N = 10**4
COMB = 3 * 10**4


def comb(rng, n):
    spine = n // 2
    left, right = [None] * n, [None] * n
    for i in range(spine):
        down, off = (left, right) if rng.random() < 0.5 else (right, left)
        if i + 1 < spine:
            down[i] = i + 1
        if spine + i < n:
            off[i] = spine + i
    return left, right


def generate(rng):
    shape = pick_shape(rng)
    n = COMB if shape == 2 else N
    if shape == 0:
        left, right = zigzag_path(rng, n)
    elif shape == 1:
        left, right = thin_tree(rng, n, 3)
    else:
        left, right = comb(rng, n)
    depth = [0] * n
    for i in range(n):
        for child in (left[i], right[i]):
            if child is not None:
                depth[child] = depth[i] + 1
    base = rng.randint(-(3 * 10**4), 3 * 10**4 - n)
    return {"root": level_order([base + d for d in depth], left, right)}
