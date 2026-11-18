"""Find Right Interval: a list of [start, end] intervals with unique starts."""


def check(intervals: list[list[int]]) -> None:
    assert 1 <= len(intervals) <= 2 * 10**4, "1 <= intervals.length <= 2 * 10^4"
    assert all(len(iv) == 2 for iv in intervals), "intervals[i].length == 2"
    assert all(-(10**6) <= s <= e <= 10**6 for s, e in intervals), "-10^6 <= starti <= endi <= 10^6"
    assert len({s for s, _ in intervals}) == len(intervals), (
        "the start point of each interval is unique"
    )
