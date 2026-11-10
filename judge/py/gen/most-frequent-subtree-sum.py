"""Most Frequent Subtree Sum at 10^4 nodes: a deep chain or random tree, with values from a
tiny set so many subtree sums tie."""

from collections import deque

SEEDS = 3
N = 10**4


def generate(rng):
    left, right = [None] * N, [None] * N
    chain = rng.random() < 0.4
    slots = [(0, 0), (0, 1)]
    for child in range(1, N):
        if chain:
            parent, side = child - 1, rng.randint(0, 1)
        else:
            pick = rng.randrange(len(slots))
            slots[pick], slots[-1] = slots[-1], slots[pick]
            parent, side = slots.pop()
            slots.append((child, 0))
            slots.append((child, 1))
        (right if side else left)[parent] = child
    if rng.random() < 0.5:
        vals = [rng.choice((-1, 0, 1)) for _ in range(N)]
    else:
        vals = [rng.randint(-(10**5), 10**5) for _ in range(N)]
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
