"""Paths in Maze That Lead to Same Room: n rooms and a list of corridors."""


def check(n: int, corridors: list[list[int]]) -> None:
    assert isinstance(n, int) and 2 <= n <= 1000, "2 <= n <= 1000"
    assert isinstance(corridors, list), "corridors is an array"
    assert 1 <= len(corridors) <= 5 * 10**4, "1 <= corridors.length <= 5 * 10^4"
    assert all(isinstance(c, list) and len(c) == 2 for c in corridors), "corridors[i].length == 2"
    assert all(isinstance(x, int) and 1 <= x <= n for c in corridors for x in c), (
        "1 <= room1i, room2i <= n"
    )
    assert all(a != b for a, b in corridors), "room1i != room2i"
    assert len({(min(a, b), max(a, b)) for a, b in corridors}) == len(corridors), (
        "There are no duplicate corridors"
    )
