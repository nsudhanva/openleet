"""Largest BST Subtree at the maximum 10^4 nodes: a zigzag chain that is a BST except for one
repeated value deep down, so checking each subtree top-down walks to that repeat from every
ancestor, ~4 * 10^7 visits."""

from _shapes import inorder, level_order, zigzag_path

SEEDS = 2
N = 10**4


def generate(rng):
    left, right = zigzag_path(rng, N, empty=-1)
    vals = [0] * N
    for rank, node in enumerate(inorder(left, right, empty=-1)):
        vals[node] = rank
    keys = sorted(rng.sample(range(-(10**4), 10**4 + 1), N))
    vals = [keys[v] for v in vals]
    # Node c - 1 takes its child c's value: only the subtrees from c down stay BSTs.
    c = N - rng.randint(1, N // 10)
    vals[c - 1] = vals[c]
    out = level_order(vals, left, right, empty=-1)
    return {"root": out}
