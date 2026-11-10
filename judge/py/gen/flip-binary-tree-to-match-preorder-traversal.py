"""Flip Binary Tree to Match Preorder at the maximum n = 100: voyage is the preorder after random
flips (answer exists), or that voyage with two values swapped (usually impossible)."""

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
    vals = list(range(1, N + 1))
    rng.shuffle(vals)
    voyage, stack = [], [0]
    while stack:
        u = stack.pop()
        voyage.append(vals[u])
        kids = [c for c in (left[u], right[u]) if c >= 0]
        if rng.random() < 0.5:
            kids.reverse()
        stack.extend(reversed(kids))
    if rng.random() < 0.34:
        i, j = rng.sample(range(1, N), 2)
        voyage[i], voyage[j] = voyage[j], voyage[i]
    return {"root": serialize(vals, left, right), "voyage": voyage}
