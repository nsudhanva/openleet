"""Longest Special Path II: a weighted tree given as edges [u, v, length] and node values."""


def check(edges: list[list[int]], nums: list[int]) -> None:
    n = len(nums)
    assert 2 <= n <= 5 * 10**4, "2 <= n <= 5 * 10^4"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(isinstance(e, list) and len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= u < n and 0 <= v < n for u, v, _ in edges), "0 <= ui, vi < n"
    assert all(1 <= w <= 10**3 for _, _, w in edges), "1 <= lengthi <= 10^3"
    assert all(0 <= v <= 5 * 10**4 for v in nums), "0 <= nums[i] <= 5 * 10^4"
    root = list(range(n))

    def find(x: int) -> int:
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for u, v, _ in edges:
        a, b = find(u), find(v)
        assert a != b, "edges represents a valid tree"
        root[a] = b
