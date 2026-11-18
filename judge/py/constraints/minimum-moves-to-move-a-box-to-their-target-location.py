"""Minimum Moves to Move a Box to Their Target Location: a character grid with one S, B and T."""


def check(grid: list[list[str]]) -> None:
    m = len(grid)
    assert 1 <= m <= 20, "1 <= m <= 20"
    n = len(grid[0])
    assert 1 <= n <= 20, "1 <= n <= 20"
    assert all(len(r) == n for r in grid), "n == grid[i].length"
    cells = [c for r in grid for c in r]
    assert all(c in (".", "#", "S", "T", "B") for c in cells), (
        "grid contains only characters '.', '#', 'S', 'T', or 'B'"
    )
    for ch in "SBT":
        assert cells.count(ch) == 1, f"There is only one character '{ch}' in the grid"
