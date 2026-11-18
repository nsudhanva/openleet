"""Longest Well-Performing Interval: hours worked per day."""


def check(hours: list[int]) -> None:
    assert 1 <= len(hours) <= 10**4, "1 <= hours.length <= 10^4"
    assert all(0 <= h <= 16 for h in hours), "0 <= hours[i] <= 16"
