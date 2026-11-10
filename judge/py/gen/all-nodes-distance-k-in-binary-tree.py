"""All Nodes Distance K at the maximum 500 nodes with distinct values: a chain or a random
tree, with the target in the middle so the walk goes both up and down."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 500


def generate(rng):
    left, right = shaped_tree(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = rng.sample(range(501), N)
    target = vals[rng.randrange(N // 4, 3 * N // 4)]
    k = rng.choice([rng.randint(0, 30), rng.randint(0, 500), rng.randint(0, 1000)])
    return {"root": level_order(vals, left, right), "target": target, "k": k}
