"""Count Pairs of Nodes at n = 5000 nodes, 10^4 edges (repeats allowed, a few hubs) and 20
queries, so checking every pair of nodes for every query costs 2.5 * 10^8 steps."""

SEEDS = 2
N = 5000
EDGES = 10**4
QUERIES = 20


def generate(rng):
    hubs = rng.sample(range(1, N + 1), min(10, N))
    edges = []
    while len(edges) < EDGES:
        u = rng.choice(hubs) if rng.random() < 0.2 else rng.randint(1, N)
        v = rng.randint(1, N)
        if u != v:
            edges.append([u, v])
    queries = [rng.randint(0, min(40, EDGES - 1)) for _ in range(QUERIES - 2)] + [0, EDGES - 1]
    rng.shuffle(queries)
    return {"n": N, "edges": edges, "queries": queries}
