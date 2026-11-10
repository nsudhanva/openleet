"""Check Completeness at the maximum 100 nodes: a complete tree (true), a complete tree with one
interior gap (false), or a random tree."""

from _shapes import level_order, shaped_tree

SEEDS = 3
N = 100


def generate(rng):
    shape = rng.choice(["complete", "gap", "random"])
    if shape == "random":
        left, right = shaped_tree(rng, N, "random")
        vals = [rng.randint(1, 1000) for _ in range(N)]
        return {"root": level_order(vals, left, right)}
    root = [rng.randint(1, 1000) for _ in range(N)]
    if shape == "gap":
        # Remove a leaf-level slot that is not last: insert a None before the final node.
        i = rng.randrange(64, N - 1)
        root = [*root[:i], None, *root[i : N - 1]]
    return {"root": root}
