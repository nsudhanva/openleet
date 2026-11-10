"""Delete Nodes And Return Forest on a 1000-node tree (values 1..1000): a random tree or a
long chain, deleting a random subset that splits it into many pieces."""

from _shapes import level_order, random_tree, zigzag_path

SEEDS = 2
N = 1000


def generate(rng):
    vals = rng.sample(range(1, N + 1), N)
    left, right = zigzag_path(rng, N, -1) if rng.random() < 0.5 else random_tree(rng, N, -1)
    to_delete = rng.sample(range(1, N + 1), rng.randint(50, 400))
    return {"root": level_order(vals, left, right, empty=-1), "to_delete": to_delete}
