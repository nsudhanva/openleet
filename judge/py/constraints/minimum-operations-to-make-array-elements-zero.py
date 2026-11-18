"""Minimum Operations to Make Array Elements Zero: queries, each a pair [l, r]."""


def check(queries: list[list[int]]) -> None:
    assert isinstance(queries, list), "queries is a list"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(isinstance(q, list) and len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(1 <= lo < hi <= 10**9 for lo, hi in queries), "1 <= l < r <= 10^9"
