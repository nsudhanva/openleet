"""Maximum Width of Binary Tree at 3000 nodes: a long random zigzag chain (position indices
grow to 2^2000) ending in a bushy subtree at most 30 levels deep, or a bushy tree of depth
at most 30, so the answer stays within 2^30 as guaranteed."""

from collections import deque

SEEDS = 3
N = 3000
DEPTH = 30


def generate(rng):
    left, right, depth = [None], [None], [0]
    chain = rng.choice((0, rng.randint(1000, 2500)))
    for _ in range(chain):
        child = len(left)
        left.append(None)
        right.append(None)
        depth.append(0)
        if rng.random() < 0.5:
            left[child - 1] = child
        else:
            right[child - 1] = child
    base = len(left) - 1
    open_slots = [base]
    depth[base] = 0
    while len(left) < N:
        parent = open_slots[rng.randrange(len(open_slots))]
        sides = [s for s, arr in ((0, left), (1, right)) if arr[parent] is None]
        side = rng.choice(sides)
        child = len(left)
        left.append(None)
        right.append(None)
        depth.append(depth[parent] + 1)
        (right if side else left)[parent] = child
        if len(sides) == 1:
            open_slots.remove(parent)
        if depth[child] < DEPTH:
            open_slots.append(child)
    vals = [rng.randint(-100, 100) for _ in range(N)]
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
