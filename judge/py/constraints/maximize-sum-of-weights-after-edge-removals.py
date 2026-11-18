"""Maximize Sum of Weights after Edge Removals: weighted tree edges [a, b, w] and k."""


def check(edges: list[list[int]], k: int) -> None:
    n = len(edges) + 1
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= k <= n - 1, "1 <= k <= n - 1"
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b, _ in edges), (
        "0 <= edges[i][0], edges[i][1] <= n - 1"
    )
    assert all(1 <= w <= 10**6 for _, _, w in edges), "1 <= edges[i][2] <= 10^6"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b, _ in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "edges form a valid tree"
        parent[ra] = rb
