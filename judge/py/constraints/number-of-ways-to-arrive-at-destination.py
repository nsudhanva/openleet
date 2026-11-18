"""Number of Ways to Arrive at Destination: n intersections and weighted undirected roads."""


def check(n: int, roads: list[list[int]]) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert isinstance(roads, list), "roads is a list"
    assert n - 1 <= len(roads) <= n * (n - 1) // 2, "n - 1 <= roads.length <= n * (n - 1) / 2"
    assert all(isinstance(r, list) and len(r) == 3 for r in roads), "roads[i].length == 3"
    assert all(all(type(x) is int for x in r) for r in roads), "roads[i] holds integers"
    assert all(0 <= u <= n - 1 and 0 <= v <= n - 1 for u, v, _ in roads), "0 <= ui, vi <= n - 1"
    assert all(1 <= t <= 10**9 for _, _, t in roads), "1 <= timei <= 10^9"
    assert all(u != v for u, v, _ in roads), "ui != vi"
    assert len({frozenset((u, v)) for u, v, _ in roads}) == len(roads), (
        "at most one road connecting any two intersections"
    )
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v, _ in roads:
        parent[find(u)] = find(v)
    assert len({find(i) for i in range(n)}) == 1, "any intersection reachable from any other"
