"""Shortest Path to Get All Keys: grid rows of letters, '.', '#' and one '@'."""


def check(grid: list[str]) -> None:
    m = len(grid)
    assert 1 <= m <= 30, "1 <= m <= 30"
    n = len(grid[0])
    assert 1 <= n <= 30, "1 <= n <= 30"
    assert all(len(row) == n for row in grid), "n == grid[i].length"
    cells = [ch for row in grid for ch in row]
    assert all(ch in ".#@" or (ch.isascii() and ch.isalpha()) for ch in cells), (
        "grid[i][j] is either an English letter, '.', '#', or '@'"
    )
    assert cells.count("@") == 1, "There is exactly one '@' in the grid"
    keys = [ch for ch in cells if ch.islower()]
    assert 1 <= len(keys) <= 6, "The number of keys in the grid is in the range [1, 6]"
    assert len(set(keys)) == len(keys), "Each key in the grid is unique"
    assert all(k.upper() in cells for k in keys), "Each key in the grid has a matching lock"
    locks = [ch for ch in cells if ch.isupper()]
    first = [chr(ord("a") + i) for i in range(len(keys))]
    assert sorted(keys) == first, "keys are the first k letters of the alphabet"
    assert sorted(locks) == [k.upper() for k in first], "exactly one lock for each key"
