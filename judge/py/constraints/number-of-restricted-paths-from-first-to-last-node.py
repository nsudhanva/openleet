"""Number of Restricted Paths From First to Last Node: a connected weighted graph on 1..n."""


def check(n: int, edges: list[list[int]]) -> None:
    assert 1 <= n <= 2 * 10**4, "1 <= n <= 2 * 10^4"
    assert n - 1 <= len(edges) <= 4 * 10**4, "n - 1 <= edges.length <= 4 * 10^4"
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(1 <= u <= n and 1 <= v <= n for u, v, _ in edges), "1 <= ui, vi <= n"
    assert all(u != v for u, v, _ in edges), "ui != vi"
    assert all(1 <= w <= 10**5 for _, _, w in edges), "1 <= weighti <= 10^5"
    pairs = {(min(u, v), max(u, v)) for u, v, _ in edges}
    assert len(pairs) == len(edges), "there is at most one edge between any two nodes"
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v, _ in edges:
        parent[find(u)] = find(v)
    assert len({find(i) for i in range(1, n + 1)}) == 1, (
        "there is at least one path between any two nodes"
    )
