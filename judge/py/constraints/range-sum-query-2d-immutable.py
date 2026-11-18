"""Range Sum Query 2D - Immutable: a matrix, then sumRegion calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "NumMatrix" and len(args[0]) == 1, "constructor takes matrix"
    matrix = args[0][0]
    m = len(matrix)
    assert 1 <= m <= 200, "1 <= m <= 200"
    n = len(matrix[0])
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(r) == n for r in matrix), "n == matrix[i].length"
    assert all(-(10**4) <= v <= 10**4 for r in matrix for v in r), "-10^4 <= matrix[i][j] <= 10^4"
    assert len(ops) - 1 <= 10**4, "at most 10^4 calls to sumRegion"
    for op, a in zip(ops[1:], args[1:], strict=False):
        assert op == "sumRegion" and len(a) == 4, "only sumRegion(row1, col1, row2, col2) is called"
        r1, c1, r2, c2 = a
        assert 0 <= r1 <= r2 < m, "0 <= row1 <= row2 < m"
        assert 0 <= c1 <= c2 < n, "0 <= col1 <= col2 < n"
