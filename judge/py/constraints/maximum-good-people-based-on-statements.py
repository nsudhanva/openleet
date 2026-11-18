"""Maximum Good People Based on Statements: an n x n matrix of statements 0, 1 or 2."""


def check(statements: list[list[int]]) -> None:
    n = len(statements)
    assert 2 <= n <= 15, "2 <= n <= 15"
    assert all(len(r) == n for r in statements), "n == statements.length == statements[i].length"
    assert all(v in (0, 1, 2) for r in statements for v in r), "statements[i][j] is 0, 1, or 2"
    assert all(statements[i][i] == 2 for i in range(n)), "statements[i][i] == 2"
