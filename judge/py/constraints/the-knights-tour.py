"""The Knight's Tour: board size m x n and a start cell (r, c) that admits a full tour."""

from functools import cache

MOVES = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]


@cache
def _tour_exists(m: int, n: int, r: int, c: int) -> bool:
    seen = [[False] * n for _ in range(m)]
    seen[r][c] = True

    def nbrs(i: int, j: int) -> list[tuple[int, int]]:
        return [
            (i + a, j + b)
            for a, b in MOVES
            if 0 <= i + a < m and 0 <= j + b < n and not seen[i + a][j + b]
        ]

    def dfs(i: int, j: int, count: int) -> bool:
        if count == m * n:
            return True
        for x, y in sorted(nbrs(i, j), key=lambda p: len(nbrs(*p))):
            seen[x][y] = True
            if dfs(x, y, count + 1):
                return True
            seen[x][y] = False
        return False

    return dfs(r, c, 1)


def check(m: int, n: int, r: int, c: int) -> None:
    assert 1 <= m <= 5 and 1 <= n <= 5, "1 <= m, n <= 5"
    assert 0 <= r <= m - 1, "0 <= r <= m - 1"
    assert 0 <= c <= n - 1, "0 <= c <= n - 1"
    assert _tour_exists(m, n, r, c), "at least one possible order of movements exists"
