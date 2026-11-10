"""Maximum Depth of Binary Tree with 10^4 nodes: a zigzag chain 10^4 deep, or a random tree."""

from _shapes import level_order, random_tree, zigzag_path

SEEDS = 2
N = 10**4


def generate(rng):
    left, right = zigzag_path(rng, N) if rng.random() < 0.5 else random_tree(rng, N)
    val = [rng.randint(-100, 100) for _ in range(N)]
    return {"root": level_order(val, left, right)}
