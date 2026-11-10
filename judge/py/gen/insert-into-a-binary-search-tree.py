"""Insert into a BST with 10^4 unique values in [-10^8, 10^8]: a bushy BST or a deep chain, with
the new value landing at the bottom of the deepest path."""

SEEDS = 3
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
        left, right = [-1] * N, [*list(range(1, N)), -1]
    else:
        left, right = build(rng, N, shape == 1)
    keys = sorted(rng.sample(range(-(10**8) + 2, 10**8 - 1, 2), N))
    vals = [0] * N
    for node, v in zip(inorder(left, right), keys, strict=False):
        vals[node] = v
    # Odd values never collide with the even keys; pick one next to a random key or past the end.
    val = rng.choice([keys[-1] + 1, keys[0] - 1, rng.choice(keys) + 1])
    return {"root": serialize(vals, left, right), "val": val}
