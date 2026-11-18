"""Minimum Time to Complete Trips: bus trip times and a trip target."""


def check(time: list[int], totalTrips: int) -> None:
    assert 1 <= len(time) <= 10**5, "1 <= time.length <= 10^5"
    assert all(1 <= v <= 10**7 for v in time), "1 <= time[i] <= 10^7"
    assert 1 <= totalTrips <= 10**7, "1 <= totalTrips <= 10^7"
