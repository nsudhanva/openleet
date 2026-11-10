"""Convert BST to Greater Tree with 10^4 unique values: a random-insertion BST, or a
degenerate chain 10^4 deep (sorted insertion order)."""

from collections import deque

SEEDS = 2
N = 10**4


def level_order(vals, left, right):
    out, q = [], deque([0])
    while q:
        u = q.popleft()
        if u < 0:
            out.append(None)
            continue
        out.append(vals[u])
        q.append(left[u])
        q.append(right[u])
    while out[-1] is None:
        out.pop()
    return out


def generate(rng):
    vals = rng.sample(range(-(10**4), 10**4 + 1), N)
    left, right = [-1] * N, [-1] * N
    if rng.random() < 0.5:
        vals.sort(reverse=rng.random() < 0.5)
        child = left if vals[0] > vals[1] else right
        for i in range(N - 1):
            child[i] = i + 1
    else:
        for i in range(1, N):
            u = 0
            while True:
                side = left if vals[i] < vals[u] else right
                if side[u] < 0:
                    side[u] = i
                    break
                u = side[u]
    return {"root": level_order(vals, left, right)}
