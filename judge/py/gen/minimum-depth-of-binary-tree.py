"""Minimum Depth of Binary Tree at 10^5 nodes: a single chain (answer n, deep recursion) or a
random tree with one shallow leaf hidden among deep ones."""

from collections import deque

SEEDS = 3
N = 10**5


def generate(rng):
    left, right = [None] * N, [None] * N
    if rng.random() < 0.5:
        for child in range(1, N):
            (right if rng.random() < 0.5 else left)[child - 1] = child
    else:
        slots = [(0, 0), (0, 1)]
        for child in range(1, N):
            pick = rng.randrange(len(slots))
            slots[pick], slots[-1] = slots[-1], slots[pick]
            parent, side = slots.pop()
            (right if side else left)[parent] = child
            slots.append((child, 0))
            slots.append((child, 1))
    vals = [rng.randint(-1000, 1000) for _ in range(N)]
    out, queue = [], deque([0])
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
