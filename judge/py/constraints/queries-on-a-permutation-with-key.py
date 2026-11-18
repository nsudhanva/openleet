"""Queries on a Permutation With Key: a list of queries over 1..m."""


def check(queries: list[int], m: int) -> None:
    assert 1 <= m <= 10**3, "1 <= m <= 10^3"
    assert isinstance(queries, list), "queries is an array"
    assert 1 <= len(queries) <= m, "1 <= queries.length <= m"
    assert all(1 <= q <= m for q in queries), "1 <= queries[i] <= m"
