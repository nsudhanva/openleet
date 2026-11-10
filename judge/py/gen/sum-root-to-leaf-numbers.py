"""Sum Root to Leaf Numbers at up to 1000 nodes and 10 levels, with digits chosen so the
total still fits in 32 bits."""

from _shapes import level_order

SEEDS = 2
N = 1000
LEVELS = 10
LIMIT = 2**31 - 1


def generate(rng):
    left, right, depth = [None] * N, [None] * N, [0] * N
    slots = [(0, 0), (0, 1)]
    count = 1
    while count < N and slots:
        j = rng.randrange(len(slots))
        slots[j], slots[-1] = slots[-1], slots[j]
        parent, side = slots.pop()
        v = count
        count += 1
        (left if side == 0 else right)[parent] = v
        depth[v] = depth[parent] + 1
        if depth[v] < LEVELS - 1:
            slots.append((v, 0))
            slots.append((v, 1))
    vals = [rng.randint(0, 9) for _ in range(count)]

    def total():
        s = 0
        stack = [(0, vals[0])]
        while stack:
            node, num = stack.pop()
            kids = [c for c in (left[node], right[node]) if c is not None]
            if not kids:
                s += num
            for c in kids:
                stack.append((c, num * 10 + vals[c]))
        return s

    # Zero the shallowest levels until the answer fits in a signed 32-bit integer.
    zero_depth = 0
    while total() > LIMIT:
        for v in range(count):
            if depth[v] == zero_depth:
                vals[v] = 0
        zero_depth += 1
    return {"root": level_order(vals, left[:count], right[:count])}
