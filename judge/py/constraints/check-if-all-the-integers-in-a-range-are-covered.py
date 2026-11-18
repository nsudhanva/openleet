"""Check if All the Integers in a Range Are Covered: [start, end] ranges and left, right."""


def check(ranges: list[list[int]], left: int, right: int) -> None:
    assert isinstance(ranges, list), "ranges is a list"
    assert 1 <= len(ranges) <= 50, "1 <= ranges.length <= 50"
    assert all(isinstance(r, list) and len(r) == 2 for r in ranges), "ranges[i].length == 2"
    assert all(1 <= a <= b <= 50 for a, b in ranges), "1 <= start[i] <= end[i] <= 50"
    assert 1 <= left <= right <= 50, "1 <= left <= right <= 50"
