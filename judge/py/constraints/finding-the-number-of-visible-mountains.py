"""Finding the Number of Visible Mountains: a list of [x, y] mountain peaks."""


def check(peaks: list[list[int]]) -> None:
    assert 1 <= len(peaks) <= 10**5, "1 <= peaks.length <= 10^5"
    assert all(len(p) == 2 for p in peaks), "peaks[i].length == 2"
    assert all(1 <= p[0] <= 10**5 and 1 <= p[1] <= 10**5 for p in peaks), "1 <= xi, yi <= 10^5"
