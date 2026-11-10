"""Sum of Left Leaves at the maximum 1000 nodes: a random shape, or a zigzag-deep tree where
many left children are leaves."""

from _shapes import level_order, random_tree

SEEDS = 3
N = 1000


def generate(rng):
    if rng.random() < 0.5:
        # A right spine where every spine node also has a left leaf.
        left, right = [None] * N, [None] * N
        v = 1
        spine = 0
        while v < N:
            left[spine] = v
            v += 1
            if v < N:
                right[spine] = v
                spine = v
                v += 1
    else:
        left, right = random_tree(rng, N)
    vals = [rng.randint(-1000, 1000) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
