"""Maximal Network Rank: n cities and a list of bidirectional roads."""


def check(n: int, roads: list[list[int]]) -> None:
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert 0 <= len(roads) <= n * (n - 1) // 2, "0 <= roads.length <= n * (n - 1) / 2"
    assert all(len(r) == 2 for r in roads), "roads[i].length == 2"
    assert all(0 <= c <= n - 1 for r in roads for c in r), "0 <= ai, bi <= n-1"
    assert all(a != b for a, b in roads), "ai != bi"
    assert len({frozenset(r) for r in roads}) == len(roads), (
        "each pair of cities has at most one road"
    )
