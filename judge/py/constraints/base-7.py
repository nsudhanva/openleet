"""Base 7: one integer."""


def check(num: int) -> None:
    assert -(10**7) <= num <= 10**7, "-10^7 <= num <= 10^7"
