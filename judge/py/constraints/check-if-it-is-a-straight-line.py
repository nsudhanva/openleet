"""Check If It Is a Straight Line: a list of distinct [x, y] points."""


def check(coordinates: list[list[int]]) -> None:
    assert 2 <= len(coordinates) <= 1000, "2 <= coordinates.length <= 1000"
    assert all(len(c) == 2 for c in coordinates), "coordinates[i].length == 2"
    assert all(-(10**4) <= v <= 10**4 for c in coordinates for v in c), (
        "-10^4 <= coordinates[i][j] <= 10^4"
    )
    assert len({tuple(c) for c in coordinates}) == len(coordinates), (
        "coordinates contains no duplicate point"
    )
