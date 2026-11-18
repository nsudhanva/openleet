"""Number of Adjacent Elements With the Same Color: array length and [index, color] queries."""


def check(n: int, queries: list[list[int]]) -> None:
    assert isinstance(n, int), "n is an integer"
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= q[0] <= n - 1 for q in queries), "0 <= index_i <= n - 1"
    assert all(1 <= q[1] <= 10**5 for q in queries), "1 <= color_i <= 10^5"
