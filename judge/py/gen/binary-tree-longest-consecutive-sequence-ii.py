"""Binary Tree Longest Consecutive Sequence II: 10^4 nodes as a root with two zigzag chains, one
falling and one rising by one per step, or a thin tree rising by one per level; or a 3 * 10^4-node
comb, a spine rising by one per level with a leaf one below each spine node (1.5 * 10^4 local
minima), so following +1 steps from every node or every minimum is ~10^8 steps."""

from _shapes import level_order, pick_shape, thin_tree

SEEDS = 3
N = 10**4
COMB = 3 * 10**4


def generate(rng):
    base = rng.randint(-(2 * 10**4), 2 * 10**4)
    shape = pick_shape(rng)
    if shape == 1:
        left, right = thin_tree(rng, N, 3)
        vals = [0] * N
        for i in range(N):
            for child in (left[i], right[i]):
                if child is not None:
                    vals[child] = vals[i] + 1
        return {"root": level_order([base - 10**4 + v for v in vals], left, right)}
    if shape == 2:
        spine = COMB // 2
        left, right = [None] * COMB, [None] * COMB
        vals = [0] * COMB
        lo = rng.randint(-(3 * 10**4) + 1, 3 * 10**4 - spine)
        for i in range(spine):
            down, off = (left, right) if rng.random() < 0.5 else (right, left)
            if i + 1 < spine:
                down[i] = i + 1
            off[i] = spine + i
            vals[i], vals[spine + i] = lo + i, lo + i - 1
        return {"root": level_order(vals, left, right)}
    left, right = [None] * N, [None] * N
    vals = [base] * N
    split = rng.randint(N // 3, 2 * N // 3)
    for start, end, step, side in ((1, split, -1, left), (split, N, 1, right)):
        side[0] = start
        for i in range(start + 1, end):
            (left if rng.random() < 0.5 else right)[i - 1] = i
        for i in range(start, end):
            vals[i] = base + step * (i - start + 1)
    return {"root": level_order(vals, left, right)}
