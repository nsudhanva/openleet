"""Path Sum III on a 1000-node tree: small values with many zeros so a huge number of downward
paths match, or a deep, nearly linear tree that makes the O(n^2) scan pay full price."""

SEEDS = 2
N = 1000


def build(rng, n, deep):
    """Random binary tree shape: children lists, node 0 is the root."""
    left, right = [-1] * n, [-1] * n
    slots = [(0, 0), (0, 1)]
    for v in range(1, n):
        if deep:
            i = len(slots) - 1 - min(len(slots) - 1, int(rng.expovariate(1.0)))
        else:
            i = rng.randrange(len(slots))
        slots[i], slots[-1] = slots[-1], slots[i]
        parent, side = slots.pop()
        (left if side == 0 else right)[parent] = v
        slots.append((v, 0))
        slots.append((v, 1))
    return left, right


def serialize(vals, left, right):
    out, queue, head = [], [0], 0
    while head < len(queue):
        v = queue[head]
        head += 1
        if v == -1:
            out.append(None)
            continue
        out.append(vals[v])
        queue.append(left[v])
        queue.append(right[v])
    while out and out[-1] is None:
        out.pop()
    return out


def generate(rng):
    deep = rng.random() < 0.5
    left, right = build(rng, N, deep)
    if rng.random() < 0.5:
        vals = [0 if rng.random() < 0.5 else rng.randint(-5, 5) for _ in range(N)]
        target = rng.randint(-3, 3)
    else:
        vals = [rng.randint(-(10**9), 10**9) for _ in range(N)]
        target = rng.randint(-1000, 1000)
    return {"root": serialize(vals, left, right), "targetSum": target}
