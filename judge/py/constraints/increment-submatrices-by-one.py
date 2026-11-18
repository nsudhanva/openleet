"""Increment Submatrices by One: n and [row1, col1, row2, col2] queries."""


def check(n: int, queries: list[list[int]]) -> None:
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert 1 <= len(queries) <= 10**4, "1 <= queries.length <= 10^4"
    assert all(len(q) == 4 for q in queries), "queries[i].length == 4"
    assert all(0 <= r1 <= r2 < n for r1, _, r2, _ in queries), "0 <= row1i <= row2i < n"
    assert all(0 <= c1 <= c2 < n for _, c1, _, c2 in queries), "0 <= col1i <= col2i < n"
