"""Increasing Order Search Tree at the maximum 100 nodes, a random or left-deep BST with unique
values in [0, 1000]."""

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


def inorder(left, right):
    order, stack, u = [], [], 0
    while stack or u >= 0:
        while u >= 0:
            stack.append(u)
            u = left[u]
        u = stack.pop()
        order.append(u)
        u = right[u]
    return order


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
    if shape == 2:
        left, right = [*list(range(1, N)), -1], [-1] * N
    else:
        left, right = build(rng, N, shape == 1)
    vals = [0] * N
    for node, v in zip(inorder(left, right), sorted(rng.sample(range(1001), N)), strict=False):
        vals[node] = v
    return {"root": serialize(vals, left, right)}
