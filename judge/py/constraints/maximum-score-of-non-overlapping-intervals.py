"""Maximum Score of Non-overlapping Intervals: [left, right, weight] triples."""


def check(intervals: list[list[int]]) -> None:
    assert 1 <= len(intervals) <= 5 * 10**4, "1 <= intervals.length <= 5 * 10^4"
    assert all(len(iv) == 3 for iv in intervals), "intervals[i].length == 3"
    assert all(1 <= lo <= r <= 10**9 for lo, r, _ in intervals), "1 <= li <= ri <= 10^9"
    assert all(1 <= w <= 10**9 for _, _, w in intervals), "1 <= weighti <= 10^9"
