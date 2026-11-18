"""Minimum Fuel Cost to Report to the Capital: tree roads between n cities and the seats per car."""


def check(roads: list[list[int]], seats: int) -> None:
    n = len(roads) + 1
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(len(r) == 2 for r in roads), "roads[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in roads), "0 <= ai, bi < n"
    assert all(a != b for a, b in roads), "ai != bi"
    assert 1 <= seats <= 10**5, "1 <= seats <= 10^5"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in roads:
        ra, rb = find(a), find(b)
        assert ra != rb, "roads represents a valid tree"
        parent[ra] = rb
