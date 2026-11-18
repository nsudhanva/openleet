"""Range Product Queries of Powers: n and [start, end] queries over its power-of-two array."""


def check(n: int, queries: list[list[int]]) -> None:
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    size = bin(n).count("1")
    assert all(0 <= s <= e < size for s, e in queries), "0 <= starti <= endi < powers.length"
