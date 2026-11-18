"""Range Sum Query 2D - Mutable: a matrix, then sumRegion and update calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "NumMatrix" and len(args[0]) == 1, "constructor takes matrix"
    matrix = args[0][0]
    m = len(matrix)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(matrix[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert all(-1000 <= v <= 1000 for r in matrix for v in r), "-1000 <= matrix[i][j] <= 1000"
    assert len(ops) - 1 <= 5000, "at most 5000 calls"
    for op, a in zip(ops[1:], args[1:], strict=False):
        if op == "sumRegion":
            assert len(a) == 4, "sumRegion(row1, col1, row2, col2)"
            r1, c1, r2, c2 = a
            assert 0 <= r1 <= r2 < m, "0 <= row1 <= row2 < m"
            assert 0 <= c1 <= c2 < n, "0 <= col1 <= col2 < n"
        else:
            assert op == "update" and len(a) == 3, "only sumRegion and update are called"
            row, col, val = a
            assert 0 <= row < m, "0 <= row < m"
            assert 0 <= col < n, "0 <= col < n"
            assert -1000 <= val <= 1000, "-1000 <= val <= 1000"
