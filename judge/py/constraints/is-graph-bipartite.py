"""Is Graph Bipartite: an undirected graph as adjacency lists."""


def check(graph: list[list[int]]) -> None:
    assert isinstance(graph, list) and all(isinstance(a, list) for a in graph), "graph is a 2D list"
    n = len(graph)
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(0 <= len(a) < n for a in graph), "0 <= graph[u].length < n"
    assert all(0 <= v <= n - 1 for a in graph for v in a), "0 <= graph[u][i] <= n - 1"
    assert all(u not in a for u, a in enumerate(graph)), "graph[u] does not contain u"
    assert all(len(set(a)) == len(a) for a in graph), "all the values of graph[u] are unique"
    sets = [set(a) for a in graph]
    assert all(u in sets[v] for u, a in enumerate(graph) for v in a), (
        "if graph[u] contains v, then graph[v] contains u"
    )
