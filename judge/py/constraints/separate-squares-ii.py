"""Separate Squares II: axis-aligned squares given as [x, y, side length]."""


def check(squares: list[list[int]]) -> None:
    assert 1 <= len(squares) <= 5 * 10**4, "1 <= squares.length <= 5 * 10^4"
    assert all(len(q) == 3 for q in squares), "squares[i].length == 3"
    assert all(0 <= x <= 10**9 and 0 <= y <= 10**9 for x, y, _ in squares), "0 <= xi, yi <= 10^9"
    assert all(1 <= li <= 10**9 for _, _, li in squares), "1 <= li <= 10^9"
    assert sum(li * li for _, _, li in squares) <= 10**15, "total area of all squares <= 10^15"
