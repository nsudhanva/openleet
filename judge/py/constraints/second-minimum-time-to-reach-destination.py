"""Second Minimum Time to Reach Destination: a connected simple undirected graph on 1..n plus
travel time and signal change."""


def check(n: int, edges: list[list[int]], time: int, change: int) -> None:
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
    m = len(edges)
    assert n - 1 <= m <= min(2 * 10**4, n * (n - 1) // 2), (
        "n - 1 <= edges.length <= min(2 * 10^4, n * (n - 1) / 2)"
    )
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(1 <= u <= n and 1 <= v <= n for u, v in edges), "1 <= ui, vi <= n"
    assert all(u != v for u, v in edges), "ui != vi"
    assert len({(min(u, v), max(u, v)) for u, v in edges}) == m, "there are no duplicate edges"
    assert 1 <= time <= 10**3 and 1 <= change <= 10**3, "1 <= time, change <= 10^3"
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    comps = n
    for u, v in edges:
        a, b = find(u), find(v)
        if a != b:
            parent[a] = b
            comps -= 1
    assert comps == 1, "each vertex can be reached from every other vertex"
