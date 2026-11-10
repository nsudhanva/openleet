"""Find Mode in BST with 10^4 nodes holding many repeated values but one strict mode, in a bushy
or a deep, nearly linear shape."""

from _shapes import inorder, level_order, random_tree, thin_tree

SEEDS = 3
N = 10**4


def generate(rng):
    left, right = thin_tree(rng, N, 2, -1) if rng.random() < 0.5 else random_tree(rng, N, -1)
    mode_count = rng.choice([6, 60])
    counts = []
    remaining = N - mode_count
    while remaining > 0:
        c = min(remaining, rng.randint(1, mode_count - 1))
        counts.append(c)
        remaining -= c
    counts.insert(rng.randrange(len(counts) + 1), mode_count)
    keys = sorted(rng.sample(range(-(10**5), 10**5 + 1), len(counts)))
    values = [k for k, c in zip(keys, counts, strict=False) for _ in range(c)]
    vals = [0] * N
    for node, v in zip(inorder(left, right, empty=-1), values, strict=False):
        vals[node] = v
    return {"root": level_order(vals, left, right, empty=-1)}
