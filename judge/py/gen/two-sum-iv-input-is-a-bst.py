"""Two Sum IV at 10^4 BST nodes: a degenerate chain or a random BST, with k either a real
pair sum (the pair deep in the tree) or unreachable."""

from _shapes import insert_bst, level_order, pick_shape

SEEDS = 3
N = 10**4
TOP = 10**4


def generate(rng):
    shape = pick_shape(rng)
    values = rng.sample(range(-TOP, TOP + 1), N)
    if shape == 0:
        values.sort()
    left, right = insert_bst(values, range(N))
    if rng.random() < 0.5:
        x, y = rng.sample(values[-100:], 2)
        k = x + y
    else:
        k = rng.choice([10**5, -(10**5), 2 * TOP + 1])
    return {"root": level_order(values, left, right), "k": k}
