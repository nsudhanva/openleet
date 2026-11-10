"""Shortest Path Visiting All Nodes at the maximum n = 12 (2^12 masks): a path, a sparse random
connected graph, or a dense one."""

SEEDS = 3


def generate(rng):
    shape = rng.getrandbits(6) % 3
    n = 12
    adj = [set() for _ in range(n)]
    order = list(range(n))
    rng.shuffle(order)
    for i in range(1, n):
        parent = order[i - 1] if shape == 0 else order[rng.randrange(i)]
        adj[order[i]].add(parent)
        adj[parent].add(order[i])
    extra = {0: 0, 1: 4, 2: 40}[shape]
    for _ in range(extra):
        a, b = rng.randrange(n), rng.randrange(n)
        if a != b:
            adj[a].add(b)
            adj[b].add(a)
    graph = []
    for a in range(n):
        nbrs = sorted(adj[a])
        rng.shuffle(nbrs)
        graph.append(nbrs)
    return {"graph": graph}
