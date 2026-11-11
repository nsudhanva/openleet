"""Count Nodes Equal to Sum of Descendants with 2 * 10^4 nodes on one root-to-leaf path (one side
or zigzagging): zeros down to small values near the leaf, a few nodes equal to their descendants'
sum, so summing each subtree afresh, even stopping once the sum passes the node, costs 2 * 10^8
steps."""

from _shapes import level_order, zigzag_path

SEEDS = 2
N = 2 * 10**4
BOTTOM = N // 20
TOP = N // 100


def generate(rng):
    if rng.random() < 0.5:
        left, right = zigzag_path(rng, N)
    else:
        left, right = [None] * N, [*range(1, N), None]
        if rng.random() < 0.5:
            left, right = right, left
    # Node i's descendants are exactly the nodes after it on the path.
    vals, below = [0] * N, 0
    for i in range(N - 1, -1, -1):
        if i >= N - BOTTOM:
            vals[i] = below if below <= 5 * 10**4 and rng.random() < 0.01 else rng.randint(0, 3)
        elif i < TOP and below <= 10**5 and rng.random() < 0.05:
            vals[i] = below
        below += vals[i]
    return {"root": level_order(vals, left, right)}
