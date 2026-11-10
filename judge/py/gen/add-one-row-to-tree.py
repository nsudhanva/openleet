"""Add One Row to Tree at 10^4 nodes: a chain 10^4 deep (recursion-depth worst case), a deep
mostly-chain tree, or a random tree, with depth anywhere from 1 to tree depth + 1."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 10**4


def _depth(left, right):
    best, stack = 0, [(0, 1)]
    while stack:
        node, d = stack.pop()
        best = max(best, d)
        for child in (left[node], right[node]):
            if child is not None:
                stack.append((child, d + 1))
    return best


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = [rng.randint(-100, 100) for _ in range(N)]
    tree_depth = _depth(left, right)
    depth = tree_depth + 1 if rng.random() < 0.5 else rng.randint(1, tree_depth + 1)
    return {
        "root": level_order(vals, left, right),
        "val": rng.randint(-(10**5), 10**5),
        "depth": depth,
    }
