"""Insert Interval: sorted non-overlapping intervals and a new interval."""

from itertools import pairwise


def check(intervals: list[list[int]], newInterval: list[int]) -> None:
    assert 0 <= len(intervals) <= 10**4, "0 <= intervals.length <= 10^4"
    assert all(len(r) == 2 for r in intervals), "intervals[i].length == 2"
    assert all(0 <= s <= e <= 10**5 for s, e in intervals), "0 <= starti <= endi <= 10^5"
    assert all(a[0] <= b[0] for a, b in pairwise(intervals)), (
        "intervals is sorted by starti in ascending order"
    )
    assert all(a[1] < b[0] for a, b in pairwise(intervals)), "intervals are non-overlapping"
    assert len(newInterval) == 2, "newInterval.length == 2"
    assert 0 <= newInterval[0] <= newInterval[1] <= 10**5, "0 <= start <= end <= 10^5"
