"""Meeting Rooms: a list of [start, end] meeting intervals."""


def check(intervals: list[list[int]]) -> None:
    assert 0 <= len(intervals) <= 10**4, "0 <= intervals.length <= 10^4"
    assert all(len(i) == 2 for i in intervals), "intervals[i].length == 2"
    assert all(0 <= s < e <= 10**6 for s, e in intervals), "0 <= starti < endi <= 10^6"
