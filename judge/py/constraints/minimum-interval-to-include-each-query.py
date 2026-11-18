"""Minimum Interval to Include Each Query: closed intervals and query points."""


def check(intervals: list[list[int]], queries: list[int]) -> None:
    assert 1 <= len(intervals) <= 10**5, "1 <= intervals.length <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(iv) == 2 for iv in intervals), "intervals[i].length == 2"
    assert all(1 <= lo <= hi <= 10**7 for lo, hi in intervals), "1 <= left_i <= right_i <= 10^7"
    assert all(1 <= q <= 10**7 for q in queries), "1 <= queries[j] <= 10^7"
