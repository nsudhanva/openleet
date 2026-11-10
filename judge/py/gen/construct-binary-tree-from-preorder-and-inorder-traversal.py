"""Build a tree from inorder and preorder traversals at 3000 distinct values: a chain 3000
deep (recursion and linear-index-search worst case), a deep mostly-chain tree, or a random tree."""

from _shapes import shaped_tree, traversals

SEEDS = 3
N = 3000


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = rng.sample(range(-3000, 3001), N)
    pre, ino, _ = traversals(left, right)
    return {"preorder": [vals[i] for i in pre], "inorder": [vals[i] for i in ino]}
