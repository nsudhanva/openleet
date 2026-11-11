"""Minimize Maximum Component Cost with 10^4 nodes, 2 * 10^4 distinct-weight edges and k between
n / 3 and n / 2, so the answer sits mid-rank and rebuilding the components for each candidate
weight, from either end, is quadratic."""

SEEDS = 2
N = 10**4
M = 2 * 10**4
LIMIT = 10**6


def generate(rng):
    order = list(range(N))
    rng.shuffle(order)
    edges = [(order[rng.randrange(i)], order[i]) for i in range(1, N)]
    pairs = {(min(u, v), max(u, v)) for u, v in edges}
    while len(edges) < M:
        u, v = rng.sample(range(N), 2)
        if (min(u, v), max(u, v)) not in pairs:
            pairs.add((min(u, v), max(u, v)))
            edges.append((u, v))
    rng.shuffle(edges)
    weights = rng.sample(range(1, LIMIT + 1), M)
    return {
        "n": N,
        "edges": [[u, v, w] for (u, v), w in zip(edges, weights, strict=True)],
        "k": rng.randint(N // 3, N // 2),
    }
