"""Search in a BST with 5000 distinct nodes: a random BST, or a 5000-deep chain (recursion
depth worst case), searching for the deepest value or an absent one."""

from _shapes import insert_bst, level_order

SEEDS = 3
N = 5000


def generate(rng):
    chain = rng.random() < 0.5
    vals = rng.sample(range(1, 10**7 + 1), N)
    if chain:
        vals.sort(reverse=rng.random() < 0.5)
    left, right = insert_bst(vals, range(N))
    present = set(vals)
    if rng.random() < 0.6:
        val = vals[-1]
    else:
        val = rng.randint(1, 10**7)
        while val in present:
            val = rng.randint(1, 10**7)
    return {"root": level_order(vals, left, right), "val": val}
