"""Walls and Gates: an m x n grid of -1 (wall), 0 (gate) or 2^31 - 1 (empty room)."""


def check(rooms: list[list[int]]) -> None:
    m = len(rooms)
    assert 1 <= m <= 250, "1 <= m <= 250"
    n = len(rooms[0])
    assert 1 <= n <= 250, "1 <= n <= 250"
    assert all(len(row) == n for row in rooms), "n == rooms[i].length"
    assert all(v in (-1, 0, 2**31 - 1) for row in rooms for v in row), (
        "rooms[i][j] is -1, 0, or 2^31 - 1"
    )
