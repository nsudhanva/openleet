"""Unique Paths II: an m x n grid of 0/1 obstacle flags."""


def check(obstacleGrid: list[list[int]]) -> None:
    m = len(obstacleGrid)
    assert 1 <= m <= 100, "1 <= m <= 100"
    assert all(isinstance(r, list) for r in obstacleGrid), "obstacleGrid[i] is a list"
    n = len(obstacleGrid[0])
    assert 1 <= n <= 100, "1 <= n <= 100"
    assert all(len(r) == n for r in obstacleGrid), "n == obstacleGrid[i].length"
    assert all(v in (0, 1) for r in obstacleGrid for v in r), "obstacleGrid[i][j] is 0 or 1"
    ways = [0] * n
    ways[0] = 1
    for row in obstacleGrid:
        for j in range(n):
            if row[j] == 1:
                ways[j] = 0
            elif j:
                ways[j] += ways[j - 1]
    assert ways[-1] <= 2 * 10**9, "the answer is at most 2 * 10^9"
