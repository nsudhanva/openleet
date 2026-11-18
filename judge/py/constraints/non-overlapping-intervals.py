"""Non-overlapping Intervals: a list of [start, end] intervals."""


def check(intervals: list[list[int]]) -> None:
    assert 1 <= len(intervals) <= 10**5, "1 <= intervals.length <= 10^5"
    assert all(len(iv) == 2 for iv in intervals), "intervals[i].length == 2"
    assert all(-5 * 10**4 <= s < e <= 5 * 10**4 for s, e in intervals), (
        "-5 * 10^4 <= starti < endi <= 5 * 10^4"
    )
