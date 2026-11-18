"""Find the Maximum Sum of Node Values: node values, a XOR key k and the edges of a tree."""


def check(nums: list[int], k: int, edges: list[list[int]]) -> None:
    n = len(nums)
    assert 2 <= n <= 2 * 10**4, "2 <= n == nums.length <= 2 * 10^4"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[i] <= 10^9"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in edges), (
        "0 <= edges[i][0], edges[i][1] <= n - 1"
    )
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "edges represent a valid tree"
        parent[ra] = rb
