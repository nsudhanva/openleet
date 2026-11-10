"""Longest Univalue Path on 10^4 nodes with depth at most 1000, values from a tiny set so
long same-value paths form (one seed is all one value)."""

SEEDS = 2
N = 10**4
MAX_DEPTH = 1000


def level_order(root, left, right, val):
    out, queue, i = [], [root], 0
    while i < len(queue):
        node = queue[i]
        i += 1
        if node is None:
            out.append(None)
            continue
        out.append(val[node])
        queue.append(left[node])
        queue.append(right[node])
    while out and out[-1] is None:
        out.pop()
    return out


def generate(rng):
    left, right, depth = [None] * N, [None] * N, [1] * N
    # A spine reaching the depth limit, then random attachments that respect it.
    spine = MAX_DEPTH
    for i in range(1, spine):
        if rng.random() < 0.5:
            left[i - 1] = i
        else:
            right[i - 1] = i
        depth[i] = i + 1
    slots = []
    for i in range(spine):
        if depth[i] < MAX_DEPTH:
            if left[i] is None:
                slots.append((i, 0))
            if right[i] is None:
                slots.append((i, 1))
    for i in range(spine, N):
        j = rng.randrange(len(slots))
        slots[j], slots[-1] = slots[-1], slots[j]
        parent, side = slots.pop()
        if side == 0:
            left[parent] = i
        else:
            right[parent] = i
        depth[i] = depth[parent] + 1
        if depth[i] < MAX_DEPTH:
            slots.append((i, 0))
            slots.append((i, 1))
    if rng.random() < 0.5:
        val = [rng.randint(-1000, 1000)] * N
    else:
        val = [rng.choice([1, 1, 1, 2]) for _ in range(N)]
    return {"root": level_order(0, left, right, val)}
