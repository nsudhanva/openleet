"""Maximize Active Section with Trade II: a binary string and substring queries."""


def check(s: str, queries: list[list[int]]) -> None:
    n = len(s)
    assert 1 <= n <= 10**5, "1 <= s.length <= 10^5"
    assert set(s) <= {"0", "1"}, "s[i] is either '0' or '1'"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i] = [li, ri]"
    assert all(0 <= lo <= hi < n for lo, hi in queries), "0 <= li <= ri < n"
