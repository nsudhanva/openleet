"""Battleships in a Board: an m x n grid of '.' and 'X'."""


def check(board: list[list[str]]) -> None:
    m = len(board)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(board[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in board), "n == board[i].length"
    assert all(c in (".", "X") for row in board for c in row), "board[i][j] is either '.' or 'X'"
    seen = [[False] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            if board[i][j] != "X" or seen[i][j]:
                continue
            seen[i][j] = True
            stack, cells = [(i, j)], []
            while stack:
                r, c = stack.pop()
                cells.append((r, c))
                for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
                    if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "X" and not seen[nr][nc]:
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            rows = {r for r, _ in cells}
            cols = {c for _, c in cells}
            assert len(rows) == 1 or len(cols) == 1, (
                "battleships are 1 x k or k x 1 and no two are adjacent"
            )
