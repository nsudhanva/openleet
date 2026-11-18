"""Cat and Mouse: an undirected graph as adjacency lists; mouse at 1, cat at 2, hole at 0."""


def check(graph: list[list[int]]) -> None:
    assert isinstance(graph, list), "graph is a list"
    n = len(graph)
    assert 3 <= n <= 50, "3 <= graph.length <= 50"
    assert all(isinstance(g, list) for g in graph), "graph[i] is a list"
    assert all(1 <= len(g) < n for g in graph), "1 <= graph[i].length < graph.length"
    assert all(0 <= v < n for g in graph for v in g), "0 <= graph[i][j] < graph.length"
    assert all(v != i for i, g in enumerate(graph) for v in g), "graph[i][j] != i"
    assert all(len(set(g)) == len(g) for g in graph), "graph[i] is unique"
    sets = [set(g) for g in graph]
    assert all(i in sets[v] for i, g in enumerate(graph) for v in g), "the graph is undirected"
