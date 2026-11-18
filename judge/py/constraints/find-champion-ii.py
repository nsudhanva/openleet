"""Find Champion II: n teams and directed "a is stronger than b" edges forming a DAG."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert 0 <= len(edges) <= n * (n - 1) // 2, "0 <= m <= n * (n - 1) / 2"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= x <= n - 1 for e in edges for x in e), "0 <= edge[i][j] <= n - 1"
    assert all(e[0] != e[1] for e in edges), "edges[i][0] != edges[i][1]"
    pairs = {(a, b) for a, b in edges}
    assert all((b, a) not in pairs for a, b in pairs), (
        "if a is stronger than b, b is not stronger than a"
    )
    indeg = [0] * n
    adj: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        indeg[b] += 1
    stack = [v for v in range(n) if indeg[v] == 0]
    seen = 0
    while stack:
        v = stack.pop()
        seen += 1
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    assert seen == n, "stronger-than is transitive and asymmetric, so the edges have no cycle"
