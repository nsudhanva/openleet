"""Count Nodes With the Highest Score at n = 10^4: a deep skewed or a long thin binary tree with
shuffled labels, so removing each node and measuring the pieces by search, or summing each
node's subtree afresh, costs over 10^7 steps."""

from _shapes import skewed_tree, thin_tree

SEEDS = 2
N = 10**4


def generate(rng):
    if rng.random() < 0.5:
        left, right = skewed_tree(rng, N)
    else:
        left, right = thin_tree(rng, N, 3)
    labels = [0, *rng.sample(range(1, N), N - 1)]
    parents = [-1] * N
    for v in range(N):
        for child in (left[v], right[v]):
            if child is not None:
                parents[labels[child]] = labels[v]
    return {"parents": parents}
