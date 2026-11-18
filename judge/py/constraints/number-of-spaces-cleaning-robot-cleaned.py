"""Number of Spaces Cleaning Robot Cleaned: a 0/1 room grid with an empty top left."""


def check(room: list[list[int]]) -> None:
    m = len(room)
    assert 1 <= m <= 300, "1 <= m <= 300"
    n = len(room[0])
    assert all(len(row) == n for row in room), "n == room[r].length"
    assert 1 <= n <= 300, "1 <= n <= 300"
    assert all(v in (0, 1) for row in room for v in row), "room[r][c] is either 0 or 1"
    assert room[0][0] == 0, "room[0][0] == 0"
