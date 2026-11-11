"""Minimum Time for K Connected Components at n = 10^4 nodes and 2 * 10^4 edges with distinct
times and k close to n, so the answer is among the largest times and recounting the components
for each candidate time in turn is ~10^4 graph traversals."""

SEEDS = 2
N = 10**4
M = 2 * 10**4


def generate(rng):
    edges, seen = [], set()
    for v in range(1, N):
        u = rng.randrange(v)
        edges.append((u, v))
        seen.add((u, v))
    while len(edges) < M:
        u, v = sorted(rng.sample(range(N), 2))
        if (u, v) not in seen:
            seen.add((u, v))
            edges.append((u, v))
    times = rng.sample(range(1, 10**9 + 1), M)
    rng.shuffle(edges)
    k = N - rng.randrange(1, min(50, N))
    return {"n": N, "edges": [[u, v, t] for (u, v), t in zip(edges, times, strict=True)], "k": k}
