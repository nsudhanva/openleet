"""Design Tic-Tac-Toe: board size, then alternating moves on empty cells."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "ops and args have the same length"
    assert len(args[0]) == 1 and isinstance(args[0][0], int), "TicTacToe(n)"
    n = args[0][0]
    assert 2 <= n <= 100, "2 <= n <= 100"
    assert len(ops) - 1 <= n * n, "at most n^2 calls to move"
    rows = [[0, 0] for _ in range(n)]
    cols = [[0, 0] for _ in range(n)]
    diag = [[0, 0], [0, 0]]
    seen = set()
    won = False
    prev = 0
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op == "move" and len(a) == 3, "move(row, col, player)"
        assert all(isinstance(x, int) for x in a), "integer arguments"
        r, c, p = a
        assert p in (1, 2), "player is 1 or 2"
        assert 0 <= r < n and 0 <= c < n, "0 <= row, col < n"
        assert (r, c) not in seen, "(row, col) are unique for each call to move"
        assert not won, "no moves after a win"
        assert p != prev, "the two players alternate"
        seen.add((r, c))
        prev = p
        k = p - 1
        rows[r][k] += 1
        cols[c][k] += 1
        if r == c:
            diag[0][k] += 1
        if r + c == n - 1:
            diag[1][k] += 1
        won = n in (rows[r][k], cols[c][k], diag[0][k], diag[1][k])
