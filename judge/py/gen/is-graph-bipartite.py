"""Is Graph Bipartite with n = 100: a dense bipartite graph split into components, sometimes with
one odd-cycle edge added inside a side."""

SEEDS = 3
N = 100


def generate(rng):
    side = [rng.randrange(2) for _ in range(N)]
    comp = [rng.randrange(rng.choice([1, 4])) for _ in range(N)]
    p = rng.choice([0.05, 0.5])
    edges = set()
    for u in range(N):
        for v in range(u + 1, N):
            if side[u] != side[v] and comp[u] == comp[v] and rng.random() < p:
                edges.add((u, v))
    if rng.random() < 0.5:
        same = [(u, v) for u in range(N) for v in range(u + 1, N) if side[u] == side[v]]
        edges.add(rng.choice(same))
    graph = [[] for _ in range(N)]
    for u, v in sorted(edges):
        graph[u].append(v)
        graph[v].append(u)
    for row in graph:
        rng.shuffle(row)
    return {"graph": graph}
