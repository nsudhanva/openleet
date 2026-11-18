"""Minimum Amount of Time to Fill Cups: three cup counts."""


def check(amount: list[int]) -> None:
    assert len(amount) == 3, "amount.length == 3"
    assert all(0 <= a <= 100 for a in amount), "0 <= amount[i] <= 100"
