"""Remove Interval: sorted disjoint half-open intervals and one interval to remove."""

from itertools import pairwise


def check(intervals: list[list[int]], toBeRemoved: list[int]) -> None:
    assert 1 <= len(intervals) <= 10**4, "1 <= intervals.length <= 10^4"
    assert all(len(p) == 2 for p in intervals), "intervals[i] == [ai, bi]"
    assert len(toBeRemoved) == 2, "toBeRemoved == [a, b]"
    assert all(-(10**9) <= a < b <= 10**9 for a, b in intervals), "-10^9 <= ai < bi <= 10^9"
    assert all(p[1] <= q[0] for p, q in pairwise(intervals)), "intervals sorted and disjoint"
