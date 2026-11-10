"""Merge Two Binary Trees with 2000 nodes each: random shapes, or two opposite-leaning
chains that overlap only at the root (deep recursion, maximal union)."""

from collections import deque

SEEDS = 3
N = 2000
LIMIT = 10**4


def random_tree(rng, n, lean):
    """Level-order list of a random tree; lean 'left' / 'right' makes a chain."""
    left, right = [None] * n, [None] * n
    slots = [(0, 0), (0, 1)]
    for child in range(1, n):
        if lean is None:
            pick = rng.randrange(len(slots))
            slots[pick], slots[-1] = slots[-1], slots[pick]
            parent, side = slots.pop()
            slots.append((child, 0))
            slots.append((child, 1))
        else:
            parent, side = child - 1, lean
        (right if side else left)[parent] = child
    vals = [rng.randint(-LIMIT, LIMIT) for _ in range(n)]
    out, queue = [], deque([0])
    while queue:
        i = queue.popleft()
        if i is None:
            out.append(None)
            continue
        out.append(vals[i])
        queue.append(left[i])
        queue.append(right[i])
    while out and out[-1] is None:
        out.pop()
    return out


def generate(rng):
    if rng.random() < 0.5:
        return {"root1": random_tree(rng, N, None), "root2": random_tree(rng, N, None)}
    return {"root1": random_tree(rng, N, 0), "root2": random_tree(rng, N, 1)}
