"""Lowest Common Ancestor in a binary tree of 10^5 unique values: a random tree, or a deep
caterpillar (long spine with short branches) with p and q far down."""

SEEDS = 2
N = 10**5
LIMIT = 10**9


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
        p, q = rng.sample(range(N), 2)
    else:
        spine = N // 2
        for i in range(1, spine):
            if rng.random() < 0.5:
                left[i - 1] = i
            else:
                right[i - 1] = i
        for i in range(spine, N):
            host = i - spine
            if left[host] is None:
                left[host] = i
            else:
                right[host] = i
        p = rng.randrange(spine - 1000, spine)
        q = rng.randrange(N - 1000, N)
    val = rng.sample(range(-LIMIT, LIMIT + 1), N)
    return {"root": level_order(0, left, right, val), "p": val[p], "q": val[q]}
