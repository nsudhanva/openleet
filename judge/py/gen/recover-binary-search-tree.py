"""Recover BST at 1000 nodes with full 32-bit values: a random or deep BST with two swapped
values, either far apart or adjacent in sorted order."""

SEEDS = 3
N = 1000


def generate(rng):
    vals = rng.sample(range(-(2**31), 2**31), N)
    left, right = [-1] * N, [-1] * N
    if rng.random() < 0.5:
        order = list(range(N))
    else:
        # Nearly sorted insertion order gives a deep, path-like tree.
        order = sorted(range(N), key=lambda i: vals[i])
        for _ in range(N // 20):
            i = rng.randrange(N - 1)
            order[i], order[i + 1] = order[i + 1], order[i]
    root = order[0]
    for i in order[1:]:
        cur = root
        while True:
            side = left if vals[i] < vals[cur] else right
            if side[cur] == -1:
                side[cur] = i
                break
            cur = side[cur]
    by_val = sorted(range(N), key=lambda i: vals[i])
    if rng.random() < 0.5:
        k = rng.randrange(N - 1)
        a, b = by_val[k], by_val[k + 1]
    else:
        a, b = rng.sample(range(N), 2)
    vals[a], vals[b] = vals[b], vals[a]
    out, queue, head = [], [root], 0
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
    return {"root": out}
