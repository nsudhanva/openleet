"""Find Duplicate Subtrees with 5000 nodes and values from a tiny range, so most subtrees repeat:
a random bushy tree, or a deep, nearly linear one that blows up string serialization."""

SEEDS = 3
N = 5000


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
    deep = rng.random() < 0.4
    left, right = build(rng, N, deep)
    hi = rng.choice([0, 1, 2, 200])
    vals = [rng.randint(-hi, hi) for _ in range(N)]
    return {"root": serialize(vals, left, right)}
