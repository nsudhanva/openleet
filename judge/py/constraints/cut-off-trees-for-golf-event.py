"""Cut Off Trees for Golf Event: an m x n forest, 0 blocked, 1 empty, >1 distinct heights."""


def check(forest: list[list[int]]) -> None:
    m = len(forest)
    assert 1 <= m <= 50, "1 <= m <= 50"
    n = len(forest[0])
    assert 1 <= n <= 50, "1 <= n <= 50"
    assert all(len(row) == n for row in forest), "n == forest[i].length"
    assert all(0 <= v <= 10**9 for row in forest for v in row), "0 <= forest[i][j] <= 10^9"
    trees = [v for row in forest for v in row if v > 1]
    assert len(set(trees)) == len(trees), "heights of all trees are distinct"
    assert trees, "there is at least one tree to cut off"
