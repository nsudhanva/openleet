"""N-ary Tree Preorder Traversal at 10^4 nodes: a 999-deep chain with bushy
branches (deep recursion), or a wide shallow tree with one node holding thousands of
children; height stays within 1000."""

from _shapes import nary_tree

SEEDS = 3


def generate(rng):
    return {"root": nary_tree(rng, 10**4, 999)}
