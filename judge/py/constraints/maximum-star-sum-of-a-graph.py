"""Maximum Star Sum of a Graph: node values, an undirected edge list and a neighbour cap
k."""


def check(vals: list[int], edges: list[list[int]], k: int) -> None:
    n = len(vals)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in vals), "-10^4 <= vals[i] <= 10^4"
    assert 0 <= len(edges) <= min(n * (n - 1) // 2, 10**5), (
        "0 <= edges.length <= min(n * (n - 1) / 2, 10^5)"
    )
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in edges), "0 <= ai, bi <= n - 1"
    assert all(a != b for a, b in edges), "ai != bi"
    assert 0 <= k <= n - 1, "0 <= k <= n - 1"
