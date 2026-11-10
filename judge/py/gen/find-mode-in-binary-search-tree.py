"""Find Mode in BST with 10^4 nodes holding many repeated values but one strict mode, in a bushy
or a deep, nearly linear shape."""

SEEDS = 3
N = 10**4


def build(rng, n, deep):
    left, right = [-1] * n, [-1] * n
    free = [(0, 0), (0, 1)]
    for i in range(1, n):
        if deep:
            j = len(free) - 1 - rng.randrange(min(2, len(free)))
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
    left, right = build(rng, N, rng.random() < 0.5)
    mode_count = rng.choice([6, 60])
    counts = []
    remaining = N - mode_count
    while remaining > 0:
        c = min(remaining, rng.randint(1, mode_count - 1))
        counts.append(c)
        remaining -= c
    counts.insert(rng.randrange(len(counts) + 1), mode_count)
    keys = sorted(rng.sample(range(-(10**5), 10**5 + 1), len(counts)))
    values = [k for k, c in zip(keys, counts, strict=False) for _ in range(c)]
    vals = [0] * N
    for node, v in zip(inorder(left, right), values, strict=False):
        vals[node] = v
    return {"root": serialize(vals, left, right)}
