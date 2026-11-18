"""Minimum Number of Vertices to Reach All Nodes: n vertices and directed edges of a DAG."""


def check(n: int, edges: list[list[int]]) -> None:
    assert isinstance(edges, list), "edges is a list"
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= len(edges) <= min(10**5, n * (n - 1) // 2), (
        "1 <= edges.length <= min(10^5, n * (n - 1) / 2)"
    )
    assert all(isinstance(e, list) and len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= fromi, toi < n"
    assert len({(a, b) for a, b in edges}) == len(edges), "all pairs (fromi, toi) are distinct"
    indeg = [0] * n
    out: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        indeg[b] += 1
        out[a].append(b)
    stack = [v for v in range(n) if indeg[v] == 0]
    seen = 0
    while stack:
        v = stack.pop()
        seen += 1
        for w in out[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    assert seen == n, "the graph is a directed acyclic graph"
