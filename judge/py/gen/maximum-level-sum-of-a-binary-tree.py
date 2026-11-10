"""Maximum Level Sum of a Binary Tree with 10^4 nodes and values in [-10^5, 10^5]: a random
tree, or a near-complete tree with mostly negative values."""

from _shapes import level_order, random_tree

SEEDS = 2
N = 10**4
LIMIT = 10**5


def generate(rng):
    if rng.random() < 0.5:
        left, right = random_tree(rng, N)
        val = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    else:
        left, right = [None] * N, [None] * N
        for i in range(1, N):
            if i % 2:
                left[(i - 1) // 2] = i
            else:
                right[(i - 1) // 2] = i
        val = [rng.randint(-LIMIT, LIMIT // 10) for _ in range(N)]
    return {"root": level_order(val, left, right)}
