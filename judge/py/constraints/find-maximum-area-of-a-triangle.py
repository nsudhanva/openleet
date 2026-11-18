"""Find Maximum Area of a Triangle: a list of distinct [x, y] points."""


def check(coords: list[list[int]]) -> None:
    assert 1 <= len(coords) <= 10**5, "1 <= n == coords.length <= 10^5"
    assert all(len(c) == 2 for c in coords), "coords[i].length == 2"
    assert all(1 <= x <= 10**6 and 1 <= y <= 10**6 for x, y in coords), (
        "1 <= coords[i][0], coords[i][1] <= 10^6"
    )
    assert len({(x, y) for x, y in coords}) == len(coords), "all coords[i] are unique"
