"""N-ary Tree Postorder Traversal at 10^4 nodes: a 999-deep chain with bushy
branches (deep recursion), or a wide shallow tree with one node holding thousands of
children; height stays within 1000."""

from collections import deque

SEEDS = 3
N = 10**4
MAX_DEPTH = 999


def generate(rng):
    children = [[] for _ in range(N)]
    depth = [1] * N
    chain = rng.choice((MAX_DEPTH, 0, 300))
    for v in range(1, chain):
        children[v - 1].append(v)
        depth[v] = depth[v - 1] + 1
    start = max(chain, 1)
    hub = rng.random() < 0.5
    for v in range(start, N):
        if hub and rng.random() < 0.5:
            parent = 0
        else:
            parent = rng.randrange(v)
            while depth[parent] >= MAX_DEPTH:
                parent = rng.randrange(v)
        children[parent].append(v)
        depth[v] = depth[parent] + 1
    for kids in children:
        rng.shuffle(kids)
    vals = [rng.randint(0, 10**4) for _ in range(N)]
    out, queue = [vals[0], None], deque([0])
    while queue:
        node = queue.popleft()
        for child in children[node]:
            out.append(vals[child])
            queue.append(child)
        out.append(None)
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
