"""Largest Plus Sign: grid size n and a list of unique mine coordinates."""


def check(n: int, mines: list[list[int]]) -> None:
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert 1 <= len(mines) <= 5000, "1 <= mines.length <= 5000"
    assert all(len(m) == 2 for m in mines), "mines[i].length == 2"
    assert all(0 <= x < n and 0 <= y < n for x, y in mines), "0 <= xi, yi < n"
    assert len({(x, y) for x, y in mines}) == len(mines), "all the pairs (xi, yi) are unique"
