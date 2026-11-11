"""Minimum Flips in Binary Tree to Get Result: a spine of OR / AND / XOR nodes (some NOT nodes
between them), each with a leaf on one side. Seed 0 is 40 nodes of random values, so solving
each node for both target values without memoization re-solves the spine below ~2^40 times. The
other seeds are 4,000 nodes of zeros whose result must become true, so a solution that
re-evaluates the whole subtree below each node it visits does ~10^7 node visits."""

from _shapes import level_order, pick_shape

SEEDS = 3
DEPTH = 40
DEEP = 4000


def generate(rng):
    vals, left, right = [], [], []

    def node(val):
        vals.append(val)
        left.append(None)
        right.append(None)
        return len(vals) - 1

    def attach(parent, child, side):
        (left, right)[side][parent] = child

    deep = pick_shape(rng) != 0
    depth = DEEP if deep else DEPTH

    def leaf():
        return 0 if deep else rng.randint(0, 1)

    spine = node(rng.randint(2, 4))
    for level in range(depth):
        side = rng.randrange(2)
        attach(spine, node(leaf()), side)
        last = level == depth - 1
        nxt = node(leaf() if last else rng.randint(2, 4))
        if not last and not deep and rng.random() < 0.2:
            inv = node(5)
            attach(spine, inv, 1 - side)
            attach(inv, nxt, rng.randrange(2))
        else:
            attach(spine, nxt, 1 - side)
        spine = nxt
    return {"root": level_order(vals, left, right), "result": deep or rng.random() < 0.5}
