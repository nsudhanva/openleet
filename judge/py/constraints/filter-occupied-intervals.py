"""Filter Occupied Intervals: occupied [start, end] intervals and a free window."""


def check(occupiedIntervals: list[list[int]], freeStart: int, freeEnd: int) -> None:
    assert 1 <= len(occupiedIntervals) <= 5 * 10**4, "1 <= occupiedIntervals.length <= 5 * 10^4"
    assert all(len(iv) == 2 for iv in occupiedIntervals), "occupiedIntervals[i].length == 2"
    assert all(1 <= s <= e <= 10**9 for s, e in occupiedIntervals), "1 <= starti <= endi <= 10^9"
    assert 1 <= freeStart <= freeEnd <= 10**9, "1 <= freeStart <= freeEnd <= 10^9"
