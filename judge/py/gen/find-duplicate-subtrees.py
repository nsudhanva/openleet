"""Find Duplicate Subtrees with 5000 nodes and values from a tiny range, so most subtrees repeat:
a random bushy tree, or a deep, nearly linear one that blows up string serialization."""

from _shapes import level_order, random_tree, thin_tree

SEEDS = 3
N = 5000


def generate(rng):
    deep = rng.random() < 0.4
    left, right = thin_tree(rng, N, 3, -1) if deep else random_tree(rng, N, -1)
    hi = rng.choice([0, 1, 2, 200])
    vals = [rng.randint(-hi, hi) for _ in range(N)]
    return {"root": level_order(vals, left, right, empty=-1)}
