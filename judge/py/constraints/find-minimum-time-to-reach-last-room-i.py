"""Find Minimum Time to Reach Last Room I: a grid of minimum entry times."""


def check(moveTime: list[list[int]]) -> None:
    n = len(moveTime)
    assert 2 <= n <= 50, "2 <= n <= 50"
    assert all(isinstance(r, list) for r in moveTime), "moveTime is a grid"
    m = len(moveTime[0])
    assert 2 <= m <= 50, "2 <= m <= 50"
    assert all(len(r) == m for r in moveTime), "m == moveTime[i].length"
    assert all(0 <= v <= 10**9 for r in moveTime for v in r), "0 <= moveTime[i][j] <= 10^9"
