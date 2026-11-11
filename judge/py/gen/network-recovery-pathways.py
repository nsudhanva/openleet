"""Network Recovery Pathways at n = 3000 and 9000 DAG edges with distinct costs, k just above
the cheapest 0 -> n - 1 path so only low thresholds are feasible, so a shortest-path check for
every distinct cost in turn is ~9000 Dijkstras."""

SEEDS = 2
N = 3000
M = 9000


def generate(rng):
    costs = rng.sample(range(10**9 + 1), M)
    pairs = {(i, i + 1) for i in range(N - 1)}
    while len(pairs) < M:
        u, v = sorted(rng.sample(range(N), 2))
        pairs.add((u, v))
    pairs = sorted(pairs)
    rng.shuffle(pairs)
    edges = [[u, v, w] for (u, v), w in zip(pairs, costs, strict=True)]
    online = [rng.random() < 0.95 for _ in range(N)]
    online[0] = online[N - 1] = True
    graph = [[] for _ in range(N)]
    for u, v, w in edges:
        if online[u] and online[v]:
            graph[u].append((v, w))
    dist = [None] * N
    dist[0] = 0
    for u in range(N):
        if dist[u] is not None:
            for v, w in graph[u]:
                if dist[v] is None or dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
    k = (dist[N - 1] if dist[N - 1] is not None else 0) + rng.randrange(10**6)
    return {"edges": edges, "online": online, "k": k}
