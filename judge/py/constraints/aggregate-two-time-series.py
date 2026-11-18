"""Aggregate Two Time Series: two lists of [timestamp, value] sorted by timestamp."""

from itertools import pairwise


def check(series1: list[list[int]], series2: list[list[int]]) -> None:
    for s in (series1, series2):
        assert 1 <= len(s) <= 10**5, "1 <= series.length <= 10^5"
        assert all(isinstance(p, list) and len(p) == 2 for p in s), "series[i].length == 2"
        assert all(1 <= p[0] <= 10**9 for p in s), "1 <= series[i][0] <= 10^9"
        assert all(1 <= p[1] <= 10**9 for p in s), "1 <= series[i][1] <= 10^9"
        assert all(a[0] < b[0] for a, b in pairwise(s)), (
            "each series is sorted in strictly increasing order of timestamp"
        )
