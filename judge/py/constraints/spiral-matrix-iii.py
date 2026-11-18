"""Spiral Matrix III: grid size and a starting cell."""


def check(rows: int, cols: int, rStart: int, cStart: int) -> None:
    assert 1 <= rows <= 100, "1 <= rows <= 100"
    assert 1 <= cols <= 100, "1 <= cols <= 100"
    assert 0 <= rStart < rows, "0 <= rStart < rows"
    assert 0 <= cStart < cols, "0 <= cStart < cols"
