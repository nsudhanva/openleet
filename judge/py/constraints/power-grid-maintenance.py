"""Power Grid Maintenance: c stations, cables between them and type 1/2 queries."""


def check(c: int, connections: list[list[int]], queries: list[list[int]]) -> None:
    assert 1 <= c <= 10**5, "1 <= c <= 10^5"
    assert 0 <= len(connections) <= min(10**5, c * (c - 1) // 2), (
        "0 <= connections.length <= min(10^5, c * (c - 1) / 2)"
    )
    assert all(len(e) == 2 for e in connections), "connections[i].length == 2"
    assert all(1 <= u <= c and 1 <= v <= c for u, v in connections), "1 <= ui, vi <= c"
    assert all(u != v for u, v in connections), "ui != vi"
    assert 1 <= len(queries) <= 2 * 10**5, "1 <= queries.length <= 2 * 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(t in (1, 2) for t, _ in queries), "queries[i][0] is either 1 or 2"
    assert all(1 <= x <= c for _, x in queries), "1 <= queries[i][1] <= c"
