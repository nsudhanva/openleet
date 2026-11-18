"""Number of Days in a Month: a year and a month."""


def check(year: int, month: int) -> None:
    assert 1583 <= year <= 2100, "1583 <= year <= 2100"
    assert 1 <= month <= 12, "1 <= month <= 12"
