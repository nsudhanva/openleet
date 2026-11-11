"""Count Good Nodes in Binary Tree with 6 * 10^4 nodes on one root-to-leaf path (all one side or
zigzagging), values drifting upward with noise, so taking each node's path maximum afresh costs
~1.8 * 10^9 steps."""

from _shapes import level_order, zigzag_path

SEEDS = 2
N = 6 * 10**4


def generate(rng):
    if rng.random() < 0.5:
        left, right = zigzag_path(rng, N)
    else:
        left, right = [None] * N, [*range(1, N), None]
        if rng.random() < 0.5:
            left, right = right, left
    drift = 2 * 10**4 / N
    vals = [
        max(-(10**4), min(10**4, round(-(10**4) + i * drift) + rng.randint(-300, 300)))
        for i in range(N)
    ]
    return {"root": level_order(vals, left, right)}
