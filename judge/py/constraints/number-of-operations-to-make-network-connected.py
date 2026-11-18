"""Number of Operations to Make Network Connected: computers and cable connections."""


def check(n: int, connections: list[list[int]]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(connections) <= min(n * (n - 1) // 2, 10**5), (
        "1 <= connections.length <= min(n * (n - 1) / 2, 10^5)"
    )
    assert all(len(c) == 2 for c in connections), "connections[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in connections), "0 <= ai, bi < n"
    assert all(a != b for a, b in connections), "ai != bi"
    pairs = {(min(a, b), max(a, b)) for a, b in connections}
    assert len(pairs) == len(connections), "no repeated connections"
