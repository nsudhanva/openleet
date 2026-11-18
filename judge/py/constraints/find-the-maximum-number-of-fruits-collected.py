"""Find the Maximum Number of Fruits Collected: an n x n grid of fruit counts."""


def check(fruits: list[list[int]]) -> None:
    n = len(fruits)
    assert 2 <= n <= 1000, "2 <= n <= 1000"
    assert all(len(row) == n for row in fruits), "n == fruits.length == fruits[i].length"
    assert all(0 <= v <= 1000 for row in fruits for v in row), "0 <= fruits[i][j] <= 1000"
