"""Check if Grid can be Cut into Sections at 2 * 10^4 rectangles: columns of stacked bricks whose
joints interleave, so every line through them cuts a brick, under one to three full-width slabs,
so the only cuts lie at the very top and testing every edge against every rectangle is quadratic."""

from itertools import pairwise

from _shapes import pick_shape

SEEDS = 3
N = 2 * 10**4
SIZE = 10**9


def generate(rng):
    slabs = (2, 1, 3)[pick_shape(rng)]
    cols = rng.randint(2, 4)
    xs = sorted(rng.sample(range(1, SIZE), 2 * cols - 1))
    xs = [0, *xs]
    joints = sorted(rng.sample(range(SIZE * 9 // 10), N - slabs + cols))
    rects = []
    for c in range(cols):
        x1, x2 = xs[2 * c], xs[2 * c + 1]
        ys = joints[c::cols]
        rects += [[x1, a, x2, b] for a, b in pairwise(ys)]
    tops = sorted(rng.sample(range(joints[-1] + 1, SIZE + 1), slabs))
    tops = [joints[-1], *tops]
    rects += [[0, a, xs[-1], b] for a, b in pairwise(tops)]
    rng.shuffle(rects)
    return {"n": SIZE, "rectangles": rects}
