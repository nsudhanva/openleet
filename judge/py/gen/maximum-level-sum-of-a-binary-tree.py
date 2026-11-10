"""Maximum Level Sum of a Binary Tree with 10^4 nodes and values in [-10^5, 10^5]: a random
tree, or a near-complete tree with mostly negative values."""

SEEDS = 2
N = 10**4
LIMIT = 10**5


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
        val = [rng.randint(-LIMIT, LIMIT) for _ in range(N)]
    else:
        for i in range(1, N):
            if i % 2:
                left[(i - 1) // 2] = i
            else:
                right[(i - 1) // 2] = i
        val = [rng.randint(-LIMIT, LIMIT // 10) for _ in range(N)]
    return {"root": level_order(0, left, right, val)}
