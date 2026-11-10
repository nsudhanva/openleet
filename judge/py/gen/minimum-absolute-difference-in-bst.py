"""Minimum Absolute Difference in BST at 10^4 nodes with distinct values in [0, 10^5]: a
random-shape BST or a fully skewed chain."""

from collections import deque

SEEDS = 3
N = 10**4


def generate(rng):
    skew = rng.random() < 0.5
    vals = sorted(rng.sample(range(10**5 + 1), N))
    left, right = [None] * N, [None] * N
    stack = [(0, N - 1, None, False)]
    root = None
    while stack:
        lo, hi, parent, is_right = stack.pop()
        if lo > hi:
            continue
        mid = hi if skew else rng.randint(lo, hi)
        if parent is None:
            root = mid
        elif is_right:
            right[parent] = mid
        else:
            left[parent] = mid
        stack.append((lo, mid - 1, mid, False))
        stack.append((mid + 1, hi, mid, True))
    out, queue = [], deque([root])
    while queue:
        i = queue.popleft()
        if i is None:
            out.append(None)
            continue
        out.append(vals[i])
        queue.append(left[i])
        queue.append(right[i])
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
