"""Smallest Subtree with All Deepest Nodes at 500 nodes with unique values: two long chains of
equal depth (LCA at the root), a single 500-deep chain, or a random tree."""

from _shapes import level_order

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    n = 500
    left, right = [None] * n, [None] * n
    if shape == 0:
        # Root with two chains of 249 and 250 nodes; the shorter gets one more at the end.
        left[0], right[0] = 1, 2
        a, b = 1, 2
        nxt = 3
        while nxt < n:
            left[a] = nxt
            a = nxt
            nxt += 1
            if nxt < n:
                right[b] = nxt
                b = nxt
                nxt += 1
    elif shape == 1:
        for i in range(n - 1):
            if rng.random() < 0.5:
                left[i] = i + 1
            else:
                right[i] = i + 1
    else:
        free = [(0, 0), (0, 1)]
        for i in range(1, n):
            parent, side = free.pop(rng.randrange(len(free)))
            free += [(i, 0), (i, 1)]
            (left if side == 0 else right)[parent] = i
    vals = rng.sample(range(0, 501), n)
    return {"root": level_order(vals, left, right)}
