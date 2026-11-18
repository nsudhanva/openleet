"""Count Pairs of Points With Distance k: 2D integer points and k."""


def check(coordinates: list[list[int]], k: int) -> None:
    assert 2 <= len(coordinates) <= 50000, "2 <= coordinates.length <= 50000"
    assert all(len(p) == 2 for p in coordinates), "coordinates[i].length == 2"
    assert all(0 <= x <= 10**6 and 0 <= y <= 10**6 for x, y in coordinates), "0 <= xi, yi <= 10^6"
    assert 0 <= k <= 100, "0 <= k <= 100"
