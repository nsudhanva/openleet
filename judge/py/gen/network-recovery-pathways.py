"""Network Recovery Pathways at n = 3000 and 9000 DAG edges with distinct costs. Seed 0 sets k just
above the cheapest 0 -> n - 1 path, so only low thresholds are feasible and a scan from the
bottom stops early. Seed 1 keeps every node online, puts the expensive costs on the chain, allows
only skips of two to four nodes and sets k at its maximum, so thousands of thresholds are
feasible and scanning them one by one costs thousands of full Dijkstras where binary search
needs ~30."""

from _shapes import pick_shape

SEEDS = 2
N = 3000
M = 9000
K_MAX = 5 * 10**13


def generate(rng):
    high = pick_shape(rng) == 2
    costs = rng.sample(range(10**9 + 1), M)
    pairs = {(i, i + 1) for i in range(N - 1)}
    while len(pairs) < M:
        if high:  # short skips only, so every node lies between 0 and n - 1
            u = rng.randrange(N - 2)
            v = min(N - 1, u + rng.randint(2, 4))
        else:
            u, v = sorted(rng.sample(range(N), 2))
        pairs.add((u, v))
    pairs = sorted(pairs)
    rng.shuffle(pairs)
    if high:
        # The chain gets the highest costs, so a path of large minimum cost exists.
        costs.sort()
        top, rest = costs[M - (N - 1) :], costs[: M - (N - 1)]
        costs = [top.pop() if v == u + 1 else rest.pop() for u, v in pairs]
    edges = [[u, v, w] for (u, v), w in zip(pairs, costs, strict=True)]
    if high:
        return {"edges": edges, "online": [True] * N, "k": K_MAX}
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
