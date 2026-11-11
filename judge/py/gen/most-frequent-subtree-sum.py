"""Most Frequent Subtree Sum at 10^4 nodes on a chain or a tree thousands of levels deep, so
summing each subtree afresh is ~3 * 10^7 node visits; values from a tiny set make many subtree
sums tie."""

from _shapes import level_order, pick_shape, shaped_tree, skewed_tree, thin_tree

SEEDS = 3
N = 10**4


def generate(rng):
    shape = pick_shape(rng)
    if shape == 0:
        left, right = shaped_tree(rng, N, "chain")
    elif shape == 1:
        left, right = skewed_tree(rng, N, rate=0.5)
    else:
        left, right = thin_tree(rng, N, 3)
    if shape != 1:
        vals = [rng.choice((-1, 0, 1)) for _ in range(N)]
    else:
        vals = [rng.randint(-(10**5), 10**5) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
