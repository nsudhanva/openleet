"""Keys and Rooms: for each room, the list of keys found in it."""


def check(rooms: list[list[int]]) -> None:
    n = len(rooms)
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert all(0 <= len(r) <= 1000 for r in rooms), "0 <= rooms[i].length <= 1000"
    assert 1 <= sum(len(r) for r in rooms) <= 3000, "1 <= sum(rooms[i].length) <= 3000"
    assert all(0 <= v < n for r in rooms for v in r), "0 <= rooms[i][j] < n"
    assert all(len(set(r)) == len(r) for r in rooms), "all the values of rooms[i] are unique"
