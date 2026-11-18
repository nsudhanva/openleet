"""Find Missing and Repeated Values: an n x n grid holding 1..n*n with one value twice and
one missing."""

from collections import Counter


def check(grid: list[list[int]]) -> None:
    n = len(grid)
    assert 2 <= n <= 50, "2 <= n <= 50"
    assert all(len(row) == n for row in grid), "n == grid.length == grid[i].length"
    values = [v for row in grid for v in row]
    assert all(1 <= v <= n * n for v in values), "1 <= grid[i][j] <= n * n"
    counts = Counter(values)
    assert sum(c == 2 for c in counts.values()) == 1, "exactly one value appears twice"
    assert all(c <= 2 for c in counts.values()), "no value appears more than twice"
    assert len(counts) == n * n - 1, "exactly one value is missing"
