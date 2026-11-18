"""Set Intersection Size At Least Two: a list of [start, end] integer intervals."""


def check(intervals: list[list[int]]) -> None:
    assert 1 <= len(intervals) <= 3000, "1 <= intervals.length <= 3000"
    assert all(len(p) == 2 for p in intervals), "intervals[i].length == 2"
    assert all(0 <= s < e <= 10**8 for s, e in intervals), "0 <= starti < endi <= 10^8"
