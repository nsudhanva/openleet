"""Path Sum II on a 5000-node tree: a random shape with values mostly zero so many root-to-leaf
paths hit the target, or a deep, nearly linear tree."""

SEEDS = 2
N = 5000


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


def leaf_sums(vals, left, right):
    sums, stack = [], [(0, vals[0])]
    while stack:
        v, s = stack.pop()
        if left[v] == -1 and right[v] == -1:
            sums.append(s)
        for c in (left[v], right[v]):
            if c != -1:
                stack.append((c, s + vals[c]))
    return sums


def generate(rng):
    deep = rng.random() < 0.5
    left, right = build(rng, N, deep)
    vals = [0 if rng.random() < 0.7 else rng.randint(-3, 3) for _ in range(N)]
    sums = sorted(s for s in leaf_sums(vals, left, right) if -1000 <= s <= 1000)
    target = sums[len(sums) // 2] if sums else 0
    return {"root": serialize(vals, left, right), "targetSum": target}
