"""All Paths From Source to Target: adjacency lists of a DAG."""


def check(graph: list[list[int]]) -> None:
    n = len(graph)
    assert 2 <= n <= 15, "2 <= n <= 15"
    assert all(0 <= v < n for row in graph for v in row), "0 <= graph[i][j] < n"
    assert all(v != i for i, row in enumerate(graph) for v in row), "graph[i][j] != i"
    assert all(len(set(row)) == len(row) for row in graph), (
        "All the elements of graph[i] are unique"
    )
    indeg = [0] * n
    for row in graph:
        for v in row:
            indeg[v] += 1
    stack = [i for i in range(n) if indeg[i] == 0]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for v in graph[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)
    assert seen == n, "The input graph is guaranteed to be a DAG"
