"""Maximum Number of K-Divisible Components: a tree with node values and a divisor k."""


def check(n: int, edges: list[list[int]], values: list[int], k: int) -> None:
    assert 1 <= n <= 3 * 10**4, "1 <= n <= 3 * 10^4"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= ai, bi < n"
    assert len(values) == n, "values.length == n"
    assert all(0 <= v <= 10**9 for v in values), "0 <= values[i] <= 10^9"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
    assert sum(values) % k == 0, "sum of values is divisible by k"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "edges represents a valid tree"
        parent[ra] = rb
