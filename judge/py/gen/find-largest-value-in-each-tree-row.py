"""Largest Value in Each Tree Row with 10^4 nodes over the full 32-bit range: a bushy random tree
or a deep, narrow one."""

SEEDS = 2
N = 10**4


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
    left, right = build(rng, N, rng.random() < 0.5)
    vals = [rng.randint(-(2**31), 2**31 - 1) for _ in range(N)]
    return {"root": serialize(vals, left, right)}
