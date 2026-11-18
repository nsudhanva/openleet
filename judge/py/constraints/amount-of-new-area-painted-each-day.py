"""Amount of New Area Painted Each Day: [start, end) paint intervals."""


def check(paint: list[list[int]]) -> None:
    assert 1 <= len(paint) <= 10**5, "1 <= paint.length <= 10^5"
    assert all(len(p) == 2 for p in paint), "paint[i].length == 2"
    assert all(0 <= a < b <= 5 * 10**4 for a, b in paint), "0 <= starti < endi <= 5 * 10^4"
