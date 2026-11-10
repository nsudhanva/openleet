"""Maximum Sum BST in Binary Tree at 4 * 10^4 nodes: a skewed valid BST chain (deep
recursion), a random-shape BST with a few corrupted values, and a random tree."""

from _shapes import level_order, random_bst

SEEDS = 3
N = 4 * 10**4
LIMIT = 4 * 10**4


def generate(rng):
    kind = rng.choice(("chain", "corrupt", "random"))
    root, left, right = random_bst(rng, N, "right" if kind == "chain" else None)
    if kind == "random":
        vals = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    else:
        vals = sorted(rng.sample(range(-LIMIT, LIMIT + 1), N))
        if kind == "corrupt":
            for _ in range(20):
                vals[rng.randrange(N)] = rng.randint(-LIMIT, LIMIT)
    return {"root": level_order(vals, left, right, root)}
