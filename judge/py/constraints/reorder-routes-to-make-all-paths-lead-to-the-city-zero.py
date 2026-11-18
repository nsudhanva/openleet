"""Reorder Routes to Make All Paths Lead to the City Zero: a directed tree on n cities."""


def check(n: int, connections: list[list[int]]) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 2 <= n <= 5 * 10**4, "2 <= n <= 5 * 10^4"
    assert len(connections) == n - 1, "connections.length == n - 1"
    assert all(len(c) == 2 for c in connections), "connections[i].length == 2"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in connections), "0 <= ai, bi <= n - 1"
    assert all(a != b for a, b in connections), "ai != bi"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in connections:
        ra, rb = find(a), find(b)
        assert ra != rb, "the roads form a tree (only one way between two cities)"
        parent[ra] = rb
