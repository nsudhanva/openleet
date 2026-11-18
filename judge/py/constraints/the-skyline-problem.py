"""The Skyline Problem: buildings as [left, right, height], sorted by left."""


def check(buildings: list[list[int]]) -> None:
    assert 1 <= len(buildings) <= 10**4, "1 <= buildings.length <= 10^4"
    assert all(len(b) == 3 for b in buildings), "buildings[i].length == 3"
    assert all(0 <= lo < r <= 2**31 - 1 for lo, r, _ in buildings), (
        "0 <= lefti < righti <= 2^31 - 1"
    )
    assert all(1 <= h <= 2**31 - 1 for _, _, h in buildings), "1 <= heighti <= 2^31 - 1"
    assert all(buildings[i][0] <= buildings[i + 1][0] for i in range(len(buildings) - 1)), (
        "buildings is sorted by lefti in non-decreasing order"
    )
