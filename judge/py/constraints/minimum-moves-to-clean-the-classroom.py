"""Minimum Moves to Clean the Classroom: a grid of strings with one 'S', litter 'L' and energy."""


def check(classroom: list[str], energy: int) -> None:
    m = len(classroom)
    assert 1 <= m <= 20, "1 <= m == classroom.length <= 20"
    assert all(isinstance(r, str) for r in classroom), "classroom[i] is a string"
    n = len(classroom[0])
    assert 1 <= n <= 20, "1 <= n == classroom[i].length <= 20"
    assert all(len(r) == n for r in classroom), "n == classroom[i].length"
    cells = "".join(classroom)
    assert all(c in "SLRX." for c in cells), "classroom[i][j] is one of 'S', 'L', 'R', 'X', or '.'"
    assert 1 <= energy <= 50, "1 <= energy <= 50"
    assert cells.count("S") == 1, "There is exactly one 'S' in the grid"
    assert cells.count("L") <= 10, "There are at most 10 'L' cells in the grid"
