"""Race Car: a target position."""


def check(target: int) -> None:
    assert isinstance(target, int), "target is an integer"
    assert 1 <= target <= 10**4, "1 <= target <= 10^4"
