"""Validate Binary Tree Nodes at 10^4 nodes: a chain whose root has the largest label and each
node's child the next smaller one, alone (valid) or beside one isolated node (invalid), so a
search from every candidate root is ~5 * 10^7 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    left, right = [-1] * N, [-1] * N
    # Seed 0 leaves node 0 out of the chain, making two components.
    low = rng.getrandbits(1)
    for i in range(low + 1, N):
        (left if rng.random() < 0.5 else right)[i] = i - 1
    return {"n": N, "leftChild": left, "rightChild": right}
