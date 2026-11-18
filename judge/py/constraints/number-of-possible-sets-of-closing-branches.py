"""Number of Possible Sets of Closing Branches: branches and weighted undirected roads."""


def check(n: int, maxDistance: int, roads: list[list[int]]) -> None:
    assert 1 <= n <= 10, "1 <= n <= 10"
    assert 1 <= maxDistance <= 10**5, "1 <= maxDistance <= 10^5"
    assert 0 <= len(roads) <= 1000, "0 <= roads.length <= 1000"
    assert all(len(r) == 3 for r in roads), "roads[i].length == 3"
    assert all(0 <= u <= n - 1 and 0 <= v <= n - 1 for u, v, _ in roads), "0 <= ui, vi <= n - 1"
    assert all(u != v for u, v, _ in roads), "ui != vi"
    assert all(1 <= w <= 1000 for _, _, w in roads), "1 <= wi <= 1000"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v, _ in roads:
        parent[find(u)] = find(v)
    assert len({find(i) for i in range(n)}) == 1, "all branches are reachable from each other"
