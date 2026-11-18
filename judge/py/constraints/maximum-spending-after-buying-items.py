"""Maximum Spending After Buying Items: an m x n matrix of item values, each row sorted in
non-increasing order."""


def check(values: list[list[int]]) -> None:
    m = len(values)
    assert 1 <= m <= 10, "1 <= m == values.length <= 10"
    n = len(values[0])
    assert 1 <= n <= 10**4, "1 <= n == values[i].length <= 10^4"
    assert all(len(row) == n for row in values), "n == values[i].length"
    assert all(1 <= v <= 10**6 for row in values for v in row), "1 <= values[i][j] <= 10^6"
    assert all(row[j] >= row[j + 1] for row in values for j in range(n - 1)), (
        "values[i] are sorted in non-increasing order"
    )
