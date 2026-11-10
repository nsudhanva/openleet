"""Flip Equivalent Binary Trees at the maximum 100 nodes: root2 is root1 with random flips, or
additionally has two values swapped."""

SEEDS = 3
N = 100


def build(rng, n, deep):
    left, right = [-1] * n, [-1] * n
    free = [(0, 0), (0, 1)]
    for i in range(1, n):
        if deep:
            j = len(free) - 1 - rng.randrange(min(3, len(free)))
            parent, side = free.pop(j)
        else:
            j = rng.randrange(len(free))
            free[j], free[-1] = free[-1], free[j]
            parent, side = free.pop()
        (left if side == 0 else right)[parent] = i
        free.append((i, 0))
        free.append((i, 1))
    return left, right


def serialize(vals, left, right):
    out, queue, i = [], [0], 0
    while i < len(queue):
        u = queue[i]
        i += 1
        if u < 0:
            out.append(None)
            continue
        out.append(vals[u])
        queue.append(left[u])
        queue.append(right[u])
    while out[-1] is None:
        out.pop()
    return out


def generate(rng):
    left, right = build(rng, N, rng.random() < 0.3)
    vals = rng.sample(range(100), N)
    root1 = serialize(vals, left, right)
    left2, right2 = left[:], right[:]
    for u in range(N):
        if rng.random() < 0.5:
            left2[u], right2[u] = right2[u], left2[u]
    vals2 = vals[:]
    if rng.random() < 0.34:
        i, j = rng.sample(range(N), 2)
        vals2[i], vals2[j] = vals2[j], vals2[i]
    return {"root1": root1, "root2": serialize(vals2, left2, right2)}
