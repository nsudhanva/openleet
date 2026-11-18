"""Strange Printer II: an m x n grid of colors."""


def check(targetGrid: list[list[int]]) -> None:
    m = len(targetGrid)
    assert 1 <= m <= 60, "1 <= m <= 60"
    assert isinstance(targetGrid[0], list), "targetGrid is a matrix"
    n = len(targetGrid[0])
    assert 1 <= n <= 60, "1 <= n <= 60"
    assert all(len(r) == n for r in targetGrid), "n == targetGrid[i].length"
    assert all(isinstance(v, int) and 1 <= v <= 60 for r in targetGrid for v in r), (
        "1 <= targetGrid[row][col] <= 60"
    )
