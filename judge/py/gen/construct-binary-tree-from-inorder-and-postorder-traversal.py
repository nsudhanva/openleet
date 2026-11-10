"""Build a tree from inorder and postorder traversals at 3000 distinct values: a chain 3000
deep (recursion and linear-index-search worst case), a deep mostly-chain tree, or a random tree."""

from _shapes import shaped_tree, traversals

SEEDS = 3
N = 3000


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = rng.sample(range(-3000, 3001), N)
    _, ino, post = traversals(left, right)
    return {"inorder": [vals[i] for i in ino], "postorder": [vals[i] for i in post]}
