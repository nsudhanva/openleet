"""Concatenate Non-Zero Digits and Multiply by Sum II: a digit string and range queries."""


def check(s: str, queries: list[list[int]]) -> None:
    m = len(s)
    assert 1 <= m <= 10**5, "1 <= m == s.length <= 10^5"
    assert all(c in "0123456789" for c in s), "s consists of digits only"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i] = [li, ri]"
    assert all(0 <= lo <= hi < m for lo, hi in queries), "0 <= li <= ri < m"
