"""Find the Number of Distinct Colors Among the Balls: a ball limit and [ball, color] queries."""


def check(limit: int, queries: list[list[int]]) -> None:
    assert 1 <= limit <= 10**9, "1 <= limit <= 10^9"
    assert 1 <= len(queries) <= 10**5, "1 <= n == queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= q[0] <= limit for q in queries), "0 <= queries[i][0] <= limit"
    assert all(1 <= q[1] <= 10**9 for q in queries), "1 <= queries[i][1] <= 10^9"
