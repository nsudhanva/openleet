"""Count Ways to Make Array With Product: queries [n, k]."""


def check(queries: list[list[int]]) -> None:
    assert isinstance(queries, list), "queries is a list"
    assert 1 <= len(queries) <= 10**4, "1 <= queries.length <= 10^4"
    assert all(isinstance(q, list) and len(q) == 2 for q in queries), "queries[i] = [n, k]"
    assert all(1 <= n <= 10**4 and 1 <= k <= 10**4 for n, k in queries), "1 <= ni, ki <= 10^4"
