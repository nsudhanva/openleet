"""Balanced Binary Tree at 5000 nodes: a perfectly balanced tree (true, full traversal), a
chain 5000 deep (recursion-depth worst case), or a random tree."""

SEEDS = 3
N = 5000


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


def _balanced(n):
    left, right = [None] * n, [None] * n
    # Each index range [lo, hi) becomes a subtree rooted at its midpoint; ids follow creation.
    stack, nxt = [(0, n, None, 0)], 0
    while stack:
        lo, hi, parent, side = stack.pop()
        if lo >= hi:
            continue
        me = nxt
        nxt += 1
        if parent is not None:
            (left, right)[side][parent] = me
        mid = (lo + hi) // 2
        stack.append((lo, mid, me, 0))
        stack.append((mid + 1, hi, me, 1))
    return left, right


def generate(rng):
    shape = rng.choice(["balanced", "chain", "random"])
    left, right = _balanced(N) if shape == "balanced" else _shape(rng, N, shape)
    vals = [rng.randint(-(10**4), 10**4) for _ in range(N)]
    return {"root": _level_order(vals, left, right)}
