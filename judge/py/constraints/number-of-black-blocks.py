"""Number of Black Blocks: grid dimensions and distinct black cell coordinates."""


def check(m: int, n: int, coordinates: list[list[int]]) -> None:
    assert 2 <= m <= 10**5, "2 <= m <= 10^5"
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 0 <= len(coordinates) <= 10**4, "0 <= coordinates.length <= 10^4"
    assert all(len(c) == 2 for c in coordinates), "coordinates[i].length == 2"
    assert all(0 <= c[0] < m for c in coordinates), "0 <= coordinates[i][0] < m"
    assert all(0 <= c[1] < n for c in coordinates), "0 <= coordinates[i][1] < n"
    assert len({(c[0], c[1]) for c in coordinates}) == len(coordinates), (
        "coordinates are pairwise distinct"
    )
