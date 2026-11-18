"""The Time When the Network Becomes Idle: an undirected connected server graph and per-server
patience."""


def check(edges: list[list[int]], patience: list[int]) -> None:
    n = len(patience)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert patience[0] == 0, "patience[0] == 0"
    assert all(1 <= p <= 10**5 for p in patience[1:]), "1 <= patience[i] <= 10^5 for 1 <= i < n"
    assert 1 <= len(edges) <= min(10**5, n * (n - 1) // 2), (
        "1 <= edges.length <= min(10^5, n * (n - 1) / 2)"
    )
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= u < n and 0 <= v < n for u, v in edges), "0 <= ui, vi < n"
    assert all(u != v for u, v in edges), "ui != vi"
    assert len({(min(u, v), max(u, v)) for u, v in edges}) == len(edges), (
        "There are no duplicate edges"
    )
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen = [False] * n
    seen[0] = True
    stack = [0]
    while stack:
        for w in adj[stack.pop()]:
            if not seen[w]:
                seen[w] = True
                stack.append(w)
    assert all(seen), "Each server can directly or indirectly reach another server"
