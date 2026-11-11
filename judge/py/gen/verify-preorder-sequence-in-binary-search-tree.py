"""Verify Preorder Sequence in BST at 10^4 values in decreasing order, a left chain, either
valid or (seed 0) broken by the very last value, so splitting at the first larger value each time is
~5 * 10^7 steps."""

SEEDS = 2
N = 10**4


def generate(rng):
    preorder = list(range(N, 0, -1))
    if rng.getrandbits(1):
        # [.., 4, 2, 3, 1]: 3 is 2's right child, so the 1 after it is below its bound of 2.
        preorder[-3:] = [2, 3, 1]
    return {"preorder": preorder}
