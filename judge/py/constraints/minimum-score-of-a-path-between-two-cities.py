"""Minimum Score of a Path Between Two Cities: n cities and weighted undirected roads."""


def check(n: int, roads: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= len(roads) <= 10**5, "1 <= roads.length <= 10^5"
    assert all(len(r) == 3 for r in roads), "roads[i].length == 3"
    assert all(1 <= r[0] <= n and 1 <= r[1] <= n for r in roads), "1 <= ai, bi <= n"
    assert all(r[0] != r[1] for r in roads), "ai != bi"
    assert all(1 <= r[2] <= 10**4 for r in roads), "1 <= distancei <= 10^4"
    assert len({(min(r[0], r[1]), max(r[0], r[1])) for r in roads}) == len(roads), (
        "there are no repeated edges"
    )
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b, _ in roads:
        parent[find(a)] = find(b)
    assert find(1) == find(n), "there is at least one path between 1 and n"
