"""Flatten Binary Tree with the maximum 2000 nodes, bushy or a deep left-leaning chain."""

SEEDS = 3
N = 2000


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
    shape = rng.randrange(3)
    vals = [rng.randint(-100, 100) for _ in range(N)]
    if shape == 2:
        left = [*list(range(1, N)), -1]
        right = [-1] * N
    else:
        left, right = build(rng, N, shape == 1)
    return {"root": serialize(vals, left, right)}
