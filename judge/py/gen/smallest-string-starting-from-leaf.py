"""Smallest String From Leaf with 8500 nodes: a deep chain with side leaves (long strings to
compare), or a random tree of mostly equal letters so leaf strings tie for a long time."""

from _shapes import level_order

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    n = 8500
    left, right = [None] * n, [None] * n
    if shape == 0:
        # Spine of length n/2, each spine node with a leaf hanging off.
        spine = n // 2
        for i in range(spine - 1):
            left[i] = i + 1
            right[i] = spine + i
        vals = [0] * n
        for i in range(spine, n):
            vals[i] = rng.randint(0, 1)
    else:
        free = [(0, 0), (0, 1)]
        for i in range(1, n):
            parent, side = free.pop(rng.randrange(len(free)))
            free += [(i, 0), (i, 1)]
            (left if side == 0 else right)[parent] = i
        vals = [rng.choice([0, 0, 0, 1]) if shape == 1 else rng.randint(0, 25) for _ in range(n)]
    return {"root": level_order(vals, left, right)}
