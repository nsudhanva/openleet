"""Maximum Product of Splitted Binary Tree with 2 * 10^4 nodes in a zigzag chain or a deep skewed
tree, so summing each subtree separately is quadratic."""

from _shapes import level_order, skewed_tree, zigzag_path

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    left, right = zigzag_path(rng, N) if rng.random() < 0.5 else skewed_tree(rng, N, rate=0.5)
    val = [rng.randint(1, 10**4) for _ in range(N)]
    return {"root": level_order(val, left, right)}
