"""Edge Weights II on a 10^5-node tree with 10^5 queries: a random tree, or a long path-like
tree where walking each query path is quadratic."""

SEEDS = 2
N = 10**5
Q = 10**5


def generate(rng):
    deep = rng.random() < 0.5
    parent = [0, 0]
    for v in range(2, N + 1):
        if deep:
            parent.append(rng.randint(max(1, v - 3), v - 1))
        else:
            parent.append(rng.randint(1, v - 1))
    label = list(range(2, N + 1))
    rng.shuffle(label)
    label = [0, 1, *label]
    edges = [[label[parent[v]], label[v]] for v in range(2, N + 1)]
    rng.shuffle(edges)
    queries = []
    for _ in range(Q):
        u = rng.randint(1, N)
        v = u if rng.random() < 0.02 else rng.randint(1, N)
        queries.append([u, v])
    return {"edges": edges, "queries": queries}
