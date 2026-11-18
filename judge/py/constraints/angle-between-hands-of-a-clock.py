"""Angle Between Hands of a Clock: an hour and minutes."""


def check(hour: int, minutes: int) -> None:
    assert 1 <= hour <= 12, "1 <= hour <= 12"
    assert 0 <= minutes <= 59, "0 <= minutes <= 59"
