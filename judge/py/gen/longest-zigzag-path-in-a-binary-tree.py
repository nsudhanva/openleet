"""Longest ZigZag Path at 2 * 10^4 nodes: a strictly alternating path of 90% of the nodes with the
rest hung at random, so walking the zigzag from every node is ~2 * 10^8 steps."""

from _shapes import level_order

SEEDS = 2
N = 2 * 10**4


def generate(rng):
    left, right = [None] * N, [None] * N
    spine = N * 9 // 10
    side = rng.randrange(2)
    for i in range(1, spine):
        (left, right)[side][i - 1] = i
        side ^= 1
    for i in range(spine, N):
        while True:
            parent, side = rng.randrange(i), rng.randrange(2)
            if (left, right)[side][parent] is None:
                break
        (left, right)[side][parent] = i
    vals = [rng.randint(1, 100) for _ in range(N)]
    return {"root": level_order(vals, left, right)}
