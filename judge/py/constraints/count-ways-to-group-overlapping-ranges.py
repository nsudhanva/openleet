"""Count Ways to Group Overlapping Ranges: a list of [start, end] ranges."""


def check(ranges: list[list[int]]) -> None:
    assert isinstance(ranges, list), "ranges is a list"
    assert 1 <= len(ranges) <= 10**5, "1 <= ranges.length <= 10^5"
    assert all(isinstance(r, list) and len(r) == 2 for r in ranges), "ranges[i].length == 2"
    assert all(0 <= s <= e <= 10**9 for s, e in ranges), "0 <= start <= end <= 10^9"
