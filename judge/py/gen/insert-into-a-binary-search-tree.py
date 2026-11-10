"""Insert into a BST with 10^4 unique values in [-10^8, 10^8]: a bushy BST or a deep chain, with
the new value landing at the bottom of the deepest path."""

from _shapes import inorder, level_order, random_tree, thin_tree

SEEDS = 3
N = 10**4


def generate(rng):
    shape = rng.randrange(3)
    if shape == 2:
        left, right = [-1] * N, [*list(range(1, N)), -1]
    else:
        left, right = thin_tree(rng, N, 3, -1) if shape == 1 else random_tree(rng, N, -1)
    keys = sorted(rng.sample(range(-(10**8) + 2, 10**8 - 1, 2), N))
    vals = [0] * N
    for node, v in zip(inorder(left, right, empty=-1), keys, strict=False):
        vals[node] = v
    # Odd values never collide with the even keys; pick one next to a random key or past the end.
    val = rng.choice([keys[-1] + 1, keys[0] - 1, rng.choice(keys) + 1])
    return {"root": level_order(vals, left, right, empty=-1), "val": val}
