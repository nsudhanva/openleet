"""Most Profitable Path in a Tree: tree edges on nodes 0..n-1, Bob's start and gate amounts."""


def check(edges: list[list[int]], bob: int, amount: list[int]) -> None:
    n = len(edges) + 1
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= v < n for e in edges for v in e), "0 <= ai, bi < n"
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
    assert 1 <= bob < n, "1 <= bob < n"
    assert len(amount) == n, "amount.length == n"
    assert all(v % 2 == 0 and -(10**4) <= v <= 10**4 for v in amount), (
        "amount[i] is an even integer in the range [-10^4, 10^4]"
    )
