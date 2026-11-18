"""Minimum Score After Removals on a Tree: node values and the edges of a tree."""


def check(nums: list[int], edges: list[list[int]]) -> None:
    n = len(nums)
    assert 3 <= n <= 1000, "3 <= n <= 1000"
    assert all(1 <= v <= 10**8 for v in nums), "1 <= nums[i] <= 10^8"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= ai, bi < n"
    assert all(a != b for a, b in edges), "ai != bi"
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
