"""Divide Intervals Into Minimum Number of Groups: a list of [left, right] intervals."""


def check(intervals: list[list[int]]) -> None:
    assert 1 <= len(intervals) <= 10**5, "1 <= intervals.length <= 10^5"
    assert all(len(i) == 2 for i in intervals), "intervals[i].length == 2"
    assert all(1 <= lo <= hi <= 10**6 for lo, hi in intervals), "1 <= lefti <= righti <= 10^6"
