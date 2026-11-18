"""Network Recovery Pathways: a weighted DAG with online flags and a budget k."""


def check(edges: list[list[int]], online: list[bool], k: int) -> None:
    n = len(online)
    assert 2 <= n <= 5 * 10**4, "2 <= n <= 5 * 10^4"
    assert all(isinstance(b, bool) for b in online), "online[i] is either true or false"
    assert online[0] and online[n - 1], "both online[0] and online[n - 1] are true"
    assert 0 <= len(edges) <= min(10**5, n * (n - 1) // 2), (
        "0 <= m == edges.length <= min(10^5, n * (n - 1) / 2)"
    )
    assert all(len(e) == 3 for e in edges), "edges[i] = [ui, vi, costi]"
    assert all(0 <= u < n and 0 <= v < n for u, v, _ in edges), "0 <= ui, vi < n"
    assert all(u != v for u, v, _ in edges), "ui != vi"
    assert all(0 <= c <= 10**9 for _, _, c in edges), "0 <= costi <= 10^9"
    assert 0 <= k <= 5 * 10**13, "0 <= k <= 5 * 10^13"
    indeg = [0] * n
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v, _ in edges:
        adj[u].append(v)
        indeg[v] += 1
    stack = [i for i in range(n) if indeg[i] == 0]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)
    assert seen == n, "the given graph is a directed acyclic graph"
