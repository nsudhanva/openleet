"""Maximum Depth of Binary Tree with 10^4 nodes: a zigzag chain 10^4 deep, or a random tree."""

SEEDS = 2
N = 10**4


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
    left, right = [None] * N, [None] * N
    if rng.random() < 0.5:
        for i in range(1, N):
            if rng.random() < 0.5:
                left[i - 1] = i
            else:
                right[i - 1] = i
    else:
        slots = [(0, 0), (0, 1)]
        for i in range(1, N):
            j = rng.randrange(len(slots))
            slots[j], slots[-1] = slots[-1], slots[j]
            parent, side = slots.pop()
            if side == 0:
                left[parent] = i
            else:
                right[parent] = i
            slots.append((i, 0))
            slots.append((i, 1))
    val = [rng.randint(-100, 100) for _ in range(N)]
    return {"root": level_order(0, left, right, val)}
