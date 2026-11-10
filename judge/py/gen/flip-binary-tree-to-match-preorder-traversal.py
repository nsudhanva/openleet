"""Flip Binary Tree to Match Preorder at the maximum n = 100: voyage is the preorder after random
flips (answer exists), or that voyage with two values swapped (usually impossible)."""

from _shapes import level_order, random_tree, thin_tree

SEEDS = 3
N = 100


def generate(rng):
    left, right = thin_tree(rng, N, 3, -1) if rng.random() < 0.3 else random_tree(rng, N, -1)
    vals = list(range(1, N + 1))
    rng.shuffle(vals)
    voyage, stack = [], [0]
    while stack:
        u = stack.pop()
        voyage.append(vals[u])
        kids = [c for c in (left[u], right[u]) if c >= 0]
        if rng.random() < 0.5:
            kids.reverse()
        stack.extend(reversed(kids))
    if rng.random() < 0.34:
        i, j = rng.sample(range(1, N), 2)
        voyage[i], voyage[j] = voyage[j], voyage[i]
    return {"root": level_order(vals, left, right, empty=-1), "voyage": voyage}
