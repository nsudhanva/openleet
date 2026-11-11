"""Minimum Flips in Binary Tree to Get Result: a spine of 40 OR / AND / XOR nodes (with some NOT
nodes between them), each with a leaf on one side, so solving each node for both target values
without memoization re-solves the spine below ~2^40 times."""

from _shapes import level_order

SEEDS = 2
DEPTH = 40


def generate(rng):
    vals, left, right = [], [], []

    def node(val):
        vals.append(val)
        left.append(None)
        right.append(None)
        return len(vals) - 1

    def attach(parent, child, side):
        (left, right)[side][parent] = child

    spine = node(rng.randint(2, 4))
    for depth in range(DEPTH):
        side = rng.randrange(2)
        attach(spine, node(rng.randint(0, 1)), side)
        last = depth == DEPTH - 1
        nxt = node(rng.randint(0, 1) if last else rng.randint(2, 4))
        if not last and rng.random() < 0.2:
            inv = node(5)
            attach(spine, inv, 1 - side)
            attach(inv, nxt, rng.randrange(2))
        else:
            attach(spine, nxt, 1 - side)
        spine = nxt
    return {"root": level_order(vals, left, right), "result": rng.random() < 0.5}
