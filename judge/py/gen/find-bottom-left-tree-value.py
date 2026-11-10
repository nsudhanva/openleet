"""Find Bottom Left Tree Value with 10^4 nodes and full 32-bit values: a random tree, or a
zigzag chain 10^4 deep whose bottom node is on the right side."""

from _shapes import level_order

SEEDS = 2
N = 10**4


def generate(rng):
    vals = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    left, right = [-1] * N, [-1] * N
    if rng.random() < 0.5:
        for i in range(1, N):
            (left if rng.random() < 0.5 else right)[i - 1] = i
    else:
        slots = [(0, 0), (0, 1)]
        for i in range(1, N):
            j = rng.randrange(len(slots))
            slots[j], slots[-1] = slots[-1], slots[j]
            p, side = slots.pop()
            (left if side == 0 else right)[p] = i
            slots += [(i, 0), (i, 1)]
    return {"root": level_order(vals, left, right, empty=-1)}
