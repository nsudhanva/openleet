"""Sum of Matrix After Queries: matrix size n and row/column fill queries."""


def check(n: int, queries: list[list[int]]) -> None:
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 1 <= len(queries) <= 5 * 10**4, "1 <= queries.length <= 5 * 10^4"
    assert all(len(q) == 3 for q in queries), "queries[i].length == 3"
    assert all(0 <= q[0] <= 1 for q in queries), "0 <= type_i <= 1"
    assert all(0 <= q[1] < n for q in queries), "0 <= index_i < n"
    assert all(0 <= q[2] <= 10**5 for q in queries), "0 <= val_i <= 10^5"
