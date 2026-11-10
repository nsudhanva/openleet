"""Same Tree on 100-node trees (random or a skewed chain): identical, one value changed deep,
or one structural difference."""

SEEDS = 3


def build(rng, n, chain):
    left, right = [None] * n, [None] * n
    free = [(0, 0), (0, 1)]
    for i in range(1, n):
        if chain:
            parent, side = i - 1, rng.randrange(2)
        else:
            parent, side = free.pop(rng.randrange(len(free)))
            free += [(i, 0), (i, 1)]
        (left if side == 0 else right)[parent] = i
    return left, right


def level_order(vals, left, right):
    out, queue = [], [0]
    for node in queue:
        if node is None:
            out.append(None)
        else:
            out.append(vals[node])
            queue += [left[node], right[node]]
    while out and out[-1] is None:
        out.pop()
    return out


def generate(rng):
    shape = rng.getrandbits(6) % 3
    n = 100
    left, right = build(rng, n, rng.random() < 0.4)
    vals = [rng.randint(-(10**4), 10**4) for _ in range(n)]
    p = level_order(vals, left, right)
    if shape == 0:
        q = list(p)
    elif shape == 1:
        vals2 = list(vals)
        vals2[n - 1] = vals2[n - 1] + 1 if vals2[n - 1] < 10**4 else vals2[n - 1] - 1
        q = level_order(vals2, left, right)
    else:
        # Move the last node to the other side of its parent if free, else drop it.
        left2, right2 = list(left), list(right)
        for parent in range(n):
            if left2[parent] == n - 1:
                left2[parent] = None
                if right2[parent] is None:
                    right2[parent] = n - 1
                break
            if right2[parent] == n - 1:
                right2[parent] = None
                if left2[parent] is None:
                    left2[parent] = n - 1
                break
        q = level_order(vals, left2, right2)
    return {"p": p, "q": q}
