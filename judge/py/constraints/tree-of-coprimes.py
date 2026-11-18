"""Tree of Coprimes: node values and the edges of a tree rooted at node 0."""


def check(nums: list[int], edges: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(1 <= v <= 50 for v in nums), "1 <= nums[i] <= 50"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[j].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= uj, vj < n"
    assert all(a != b for a, b in edges), "uj != vj"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "the edges form a tree (no cycle, no duplicate edge)"
        parent[ra] = rb
