"""Vertical Order Traversal at the maximum 1000 nodes with few distinct values, so many nodes
share a (row, column) and the value tie-break matters; random or zigzag shapes."""

SEEDS = 3
N = 1000


def generate(rng):
    shape = rng.getrandbits(6) % 3  # seeds 0-2 land on three different shapes
    left, right = [None] * N, [None] * N
    if shape == 0:
        slots = [(0, 0), (0, 1)]
        for v in range(1, N):
            j = rng.randrange(len(slots))
            slots[j], slots[-1] = slots[-1], slots[j]
            parent, side = slots.pop()
            (left if side == 0 else right)[parent] = v
            slots.append((v, 0))
            slots.append((v, 1))
    else:
        # Zigzag spine (left, right, left, ...) with a leaf hanging off each spine node.
        v, spine, side = 1, 0, 0
        while v < N:
            (left if side == 0 else right)[spine] = v
            nxt = v
            v += 1
            if v < N:
                (right if side == 0 else left)[spine] = v
                v += 1
            spine, side = nxt, 1 - side
    hi = 3 if shape != 2 else 1000
    vals = [rng.randint(0, hi) for _ in range(N)]
    out, queue, i = [], [0], 0
    while i < len(queue):
        node = queue[i]
        i += 1
        if node is None:
            out.append(None)
            continue
        out.append(vals[node])
        queue.append(left[node])
        queue.append(right[node])
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
