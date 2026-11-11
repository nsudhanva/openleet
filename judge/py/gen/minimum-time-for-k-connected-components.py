"""Minimum Time for K Connected Components at n = 10^4 nodes and 2 * 10^4 edges with distinct
times and k close to n. One seed is a random graph whose answer is among the largest times; in the
others the largest times form a clique of 60 or 100 nodes (up to ~5,000 edges but only 99 merges),
so the answer lies beyond all of them and recounting the components for each candidate time in
turn is ~5 * 10^3 graph traversals."""

from _shapes import pick_shape

SEEDS = 3
N = 10**4
M = 2 * 10**4
CLIQUES = (0, 100, 60)


def generate(rng):
    clique = CLIQUES[pick_shape(rng)]
    members = rng.sample(range(N), clique)
    edges, seen = [], set()
    for i, a in enumerate(members):
        for b in members[:i]:
            seen.add((min(a, b), max(a, b)))
            edges.append((min(a, b), max(a, b)))
    top = len(edges)
    for v in range(1, N):
        u = rng.randrange(v)
        if (u, v) not in seen:
            edges.append((u, v))
            seen.add((u, v))
    while len(edges) < M:
        u, v = sorted(rng.sample(range(N), 2))
        if (u, v) not in seen:
            seen.add((u, v))
            edges.append((u, v))
    rest = edges[top:]
    rng.shuffle(rest)
    edges[top:] = rest
    # The clique edges get the largest times.
    times = sorted(rng.sample(range(1, 10**9 + 1), len(edges)), reverse=True)
    timed = list(zip(edges, times, strict=True))
    rng.shuffle(timed)
    k = N - clique + 1 - rng.randrange(20) if clique else N - rng.randrange(1, min(50, N))
    return {"n": N, "edges": [[u, v, t] for (u, v), t in timed], "k": k}
