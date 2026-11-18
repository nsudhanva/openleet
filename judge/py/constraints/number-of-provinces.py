"""Number of Provinces: a symmetric n x n 0/1 adjacency matrix with a 1 diagonal."""


def check(isConnected: list[list[int]]) -> None:
    n = len(isConnected)
    assert 1 <= n <= 200, "1 <= n <= 200"
    assert all(len(row) == n for row in isConnected), "n == isConnected[i].length"
    assert all(v in (0, 1) for row in isConnected for v in row), "isConnected[i][j] is 1 or 0"
    assert all(isConnected[i][i] == 1 for i in range(n)), "isConnected[i][i] == 1"
    assert all(isConnected[i][j] == isConnected[j][i] for i in range(n) for j in range(i)), (
        "isConnected[i][j] == isConnected[j][i]"
    )
