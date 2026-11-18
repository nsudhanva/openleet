"""Remove Covered Intervals: unique intervals [l, r) with l < r."""


def check(intervals: list[list[int]]) -> None:
    assert 1 <= len(intervals) <= 1000, "1 <= intervals.length <= 1000"
    assert all(len(iv) == 2 for iv in intervals), "intervals[i].length == 2"
    assert all(0 <= lo < hi <= 10**5 for lo, hi in intervals), "0 <= li < ri <= 10^5"
    assert len({tuple(iv) for iv in intervals}) == len(intervals), (
        "all the given intervals are unique"
    )
