"""Traffic Signal Color: remaining seconds on the signal."""


def check(timer: int) -> None:
    assert 0 <= timer <= 1000, "0 <= timer <= 1000"
