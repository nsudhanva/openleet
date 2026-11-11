"""Minimum Number of Vertices to Reach All Nodes on a random DAG with 5 * 10^4 nodes and edges, so
over a third of the nodes have no incoming edge and checking each node against the whole edge
list is quadratic."""

SEEDS = 2
N = 5 * 10**4
M = 5 * 10**4


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    pairs = set()
    while len(pairs) < M:
        a, b = rng.randrange(N), rng.randrange(N)
        if a != b:
            pairs.add((order[min(a, b)], order[max(a, b)]))
    edges = [list(p) for p in pairs]
    rng.shuffle(edges)
    return {"n": N, "edges": edges}
