"""Plates Between Candles: a string of '*' and '|' plus [left, right] queries."""


def check(s: str, queries: list[list[int]]) -> None:
    assert isinstance(s, str), "s is a string"
    assert 3 <= len(s) <= 10**5, "3 <= s.length <= 10^5"
    assert set(s) <= {"*", "|"}, "s consists of '*' and '|' characters"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= left <= right < len(s) for left, right in queries), (
        "0 <= lefti <= righti < s.length"
    )
