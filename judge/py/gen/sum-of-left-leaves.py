"""Sum of Left Leaves at the maximum 1000 nodes: a random shape, or a zigzag-deep tree where
many left children are leaves."""

SEEDS = 3
N = 1000


def serialize(vals, left, right, root):
    out, queue, i = [], [root], 0
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
    return out


def generate(rng):
    left, right = [None] * N, [None] * N
    if rng.random() < 0.5:
        # A right spine where every spine node also has a left leaf.
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
        slots = [(0, 0), (0, 1)]
        for v in range(1, N):
            j = rng.randrange(len(slots))
            slots[j], slots[-1] = slots[-1], slots[j]
            parent, side = slots.pop()
            (left if side == 0 else right)[parent] = v
            slots.append((v, 0))
            slots.append((v, 1))
    vals = [rng.randint(-1000, 1000) for _ in range(N)]
    return {"root": serialize(vals, left, right, 0)}
