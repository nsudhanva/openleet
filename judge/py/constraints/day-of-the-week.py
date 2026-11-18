"""Day of the Week: a day, month and year as integers."""

import calendar


def check(day: int, month: int, year: int) -> None:
    assert 1971 <= year <= 2100, "the year is between 1971 and 2100"
    assert 1 <= month <= 12, "the date is valid: 1 <= month <= 12"
    assert 1 <= day <= calendar.monthrange(year, month)[1], (
        "the date is valid: day exists in the month"
    )
