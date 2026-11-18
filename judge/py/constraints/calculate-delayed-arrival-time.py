"""Calculate Delayed Arrival Time: an arrival hour and a delay in hours."""


def check(arrivalTime: int, delayedTime: int) -> None:
    assert 1 <= arrivalTime < 24, "1 <= arrivalTime < 24"
    assert 1 <= delayedTime <= 24, "1 <= delayedTime <= 24"
