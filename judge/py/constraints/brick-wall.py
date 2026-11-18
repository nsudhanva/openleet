"""Brick Wall: rows of brick widths with equal total width."""


def check(wall: list[list[int]]) -> None:
    n = len(wall)
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert all(isinstance(r, list) for r in wall), "wall is a list of rows"
    assert all(1 <= len(r) <= 10**4 for r in wall), "1 <= wall[i].length <= 10^4"
    assert 1 <= sum(len(r) for r in wall) <= 2 * 10**4, "1 <= sum(wall[i].length) <= 2 * 10^4"
    assert all(1 <= v <= 2**31 - 1 for r in wall for v in r), "1 <= wall[i][j] <= 2^31 - 1"
    assert len({sum(r) for r in wall}) == 1, "sum(wall[i]) is the same for each row"
