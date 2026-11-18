"""Shortest Distance After Road Addition Queries I: n cities and a list of [u, v] roads to add."""


def check(n: int, queries: list[list[int]]) -> None:
    assert 3 <= n <= 500, "3 <= n <= 500"
    assert 1 <= len(queries) <= 500, "1 <= queries.length <= 500"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= u < v < n for u, v in queries), "0 <= queries[i][0] < queries[i][1] < n"
    assert all(v - u > 1 for u, v in queries), "1 < queries[i][1] - queries[i][0]"
    assert len({(u, v) for u, v in queries}) == len(queries), (
        "There are no repeated roads among the queries"
    )
