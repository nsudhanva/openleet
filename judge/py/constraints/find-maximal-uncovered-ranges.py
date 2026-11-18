"""Find Maximal Uncovered Ranges: a length n and a list of inclusive [start, end] ranges."""


def check(n: int, ranges: list[list[int]]) -> None:
    assert 1 <= n <= 10**9, "1 <= n <= 10^9"
    assert 0 <= len(ranges) <= 10**6, "0 <= ranges.length <= 10^6"
    assert all(len(r) == 2 for r in ranges), "ranges[i].length = 2"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in ranges), "0 <= ranges[i][j] <= n - 1"
    assert all(a <= b for a, b in ranges), "ranges[i][0] <= ranges[i][1]"
