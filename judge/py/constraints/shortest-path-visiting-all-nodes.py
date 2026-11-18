"""Shortest Path Visiting All Nodes: adjacency lists of a connected undirected graph."""


def check(graph: list[list[int]]) -> None:
    n = len(graph)
    assert 1 <= n <= 12, "1 <= n <= 12"
    assert all(0 <= len(nb) < n for nb in graph), "0 <= graph[i].length < n"
    assert all(0 <= v < n for nb in graph for v in nb), "graph[i] holds node labels in 0..n-1"
    assert all(i not in nb for i, nb in enumerate(graph)), "graph[i] does not contain i"
    assert all(a in graph[b] for a, nb in enumerate(graph) for b in nb), (
        "If graph[a] contains b, then graph[b] contains a"
    )
    seen = {0}
    stack = [0]
    while stack:
        for v in graph[stack.pop()]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    assert len(seen) == n, "The input graph is always connected"
