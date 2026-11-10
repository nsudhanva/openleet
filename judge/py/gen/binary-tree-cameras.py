"""Binary Tree Cameras at the maximum 1000 nodes: a chain 1000 deep, a deep mostly-chain tree,
or a random tree."""

SEEDS = 3
N = 1000


def _shape(rng, n, kind):
    """Child index lists for an n-node tree rooted at 0: 'random', 'chain' or 'deep'."""
    left, right = [None] * n, [None] * n
    slots = [(0, 0), (0, 1)]
    for i in range(1, n):
        if kind == "chain" or (kind == "deep" and rng.random() < 0.9):
            parent, side = i - 1, rng.randrange(2)
            if (left, right)[side][parent] is not None:
                side = 1 - side
        else:
            while True:
                j = rng.randrange(len(slots))
                slots[j], slots[-1] = slots[-1], slots[j]
                parent, side = slots.pop()
                if (left, right)[side][parent] is None:
                    break
        (left, right)[side][parent] = i
        slots.append((i, 0))
        slots.append((i, 1))
    return left, right


def _level_order(vals, left, right):
    out, queue, i = [], [0], 0
    while i < len(queue):
        node = queue[i]
        i += 1
        if node is None:
            out.append(None)
            continue
        out.append(vals[node])
        queue.append(left[node])
        queue.append(right[node])
    while out and out[-1] is None:
        out.pop()
    return out


def generate(rng):
    left, right = _shape(rng, N, rng.choice(["chain", "deep", "random"]))
    vals = [0] * N
    return {"root": _level_order(vals, left, right)}
