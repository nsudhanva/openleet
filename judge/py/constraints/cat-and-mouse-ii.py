"""Cat and Mouse II: a grid of strings with one each of C, M, F, plus two jump lengths."""


def check(grid: list[str], catJump: int, mouseJump: int) -> None:
    assert isinstance(grid, list) and all(isinstance(r, str) for r in grid), "grid is a list of str"
    rows = len(grid)
    assert 1 <= rows <= 8, "1 <= rows <= 8"
    cols = len(grid[0])
    assert 1 <= cols <= 8, "1 <= cols <= 8"
    assert all(len(r) == cols for r in grid), "cols = grid[i].length"
    cells = "".join(grid)
    assert all(ch in "CMF.#" for ch in cells), "grid[i][j] is one of 'C', 'M', 'F', '.', '#'"
    assert all(cells.count(ch) == 1 for ch in "CMF"), "exactly one each of 'C', 'M', 'F'"
    assert 1 <= catJump <= 8, "1 <= catJump <= 8"
    assert 1 <= mouseJump <= 8, "1 <= mouseJump <= 8"
