"""Count Covered Buildings: grid size n and unique [x, y] building coordinates."""


def check(n: int, buildings: list[list[int]]) -> None:
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert 1 <= len(buildings) <= 10**5, "1 <= buildings.length <= 10^5"
    assert all(len(b) == 2 for b in buildings), "buildings[i] = [x, y]"
    assert all(1 <= x <= n and 1 <= y <= n for x, y in buildings), "1 <= x, y <= n"
    assert len({(x, y) for x, y in buildings}) == len(buildings), "all coordinates are unique"
