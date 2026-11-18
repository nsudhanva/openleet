"""Last Day Where You Can Still Cross: a grid size and the order its cells flood."""


def check(row: int, col: int, cells: list[list[int]]) -> None:
    assert 2 <= row <= 2 * 10**4, "2 <= row <= 2 * 10^4"
    assert 2 <= col <= 2 * 10**4, "2 <= col <= 2 * 10^4"
    assert 4 <= row * col <= 2 * 10**4, "4 <= row * col <= 2 * 10^4"
    assert len(cells) == row * col, "cells.length == row * col"
    assert all(len(c) == 2 for c in cells), "cells[i].length == 2"
    assert all(1 <= r <= row and 1 <= c <= col for r, c in cells), "1 <= ri <= row, 1 <= ci <= col"
    assert len({tuple(c) for c in cells}) == len(cells), "all values of cells are unique"
