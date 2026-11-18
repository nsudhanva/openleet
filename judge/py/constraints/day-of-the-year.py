"""Day of the Year: a date string YYYY-MM-DD."""

import calendar


def check(date: str) -> None:
    assert len(date) == 10, "date.length == 10"
    assert date[4] == date[7] == "-", "date[4] == date[7] == '-'"
    digits = date[:4] + date[5:7] + date[8:]
    assert digits.isascii() and digits.isdigit(), "all other date[i]'s are digits"
    y, m, d = int(date[:4]), int(date[5:7]), int(date[8:])
    assert 1900 <= y <= 2019, "date is between Jan 1st, 1900 and Dec 31st, 2019"
    assert 1 <= m <= 12, "date is a calendar date: month"
    assert 1 <= d <= calendar.monthrange(y, m)[1], "date is a calendar date: day"
