"""Diameter of N-ary Tree with 10^4 nodes: a 900-node spine with the rest hung near its
bottom (depth at most 1000), so recomputing heights per node is ~9 * 10^6 calls."""

SEEDS = 2
N = 10**4
SPINE = 900
MAX_DEPTH = 1000


def generate(rng):
    children = [[] for _ in range(N)]
    depth = [1] * N
    for v in range(1, SPINE):
        children[v - 1].append(v)
        depth[v] = depth[v - 1] + 1
    low = SPINE * 9 // 10
    for v in range(SPINE, N):
        parent = rng.randrange(low, v)
        while depth[parent] >= MAX_DEPTH:
            parent = rng.randrange(low, v)
        children[parent].append(v)
        depth[v] = depth[parent] + 1
    for kids in children:
        rng.shuffle(kids)
    vals = [rng.randint(0, 10**4) for _ in range(N)]
    out, queue = [vals[0], None], [0]
    for node in queue:
        for child in children[node]:
            out.append(vals[child])
            queue.append(child)
        out.append(None)
    while out and out[-1] is None:
        out.pop()
    return {"root": out}
