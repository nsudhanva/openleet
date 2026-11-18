"""Pairs of Songs With Total Durations Divisible by 60: a list of song durations."""


def check(time: list[int]) -> None:
    assert 1 <= len(time) <= 6 * 10**4, "1 <= time.length <= 6 * 10^4"
    assert all(1 <= t <= 500 for t in time), "1 <= time[i] <= 500"
