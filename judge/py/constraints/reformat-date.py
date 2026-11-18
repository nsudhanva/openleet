"""Reformat Date: a date written as "Day Month Year", such as "20th Oct 2052"."""

import datetime
import re

_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_SUFFIX = {1: "st", 2: "nd", 3: "rd", 21: "st", 22: "nd", 23: "rd", 31: "st"}


def check(date: str) -> None:
    m = re.fullmatch(r"([0-9]{1,2})(st|nd|rd|th) ([A-Za-z]{3}) ([0-9]{4})", date)
    assert m, 'date has the form "Day Month Year"'
    day, suffix, month, year = int(m[1]), m[2], m[3], int(m[4])
    assert 1 <= day <= 31 and suffix == _SUFFIX.get(day, "th"), 'Day is in {"1st", ..., "31st"}'
    assert month in _MONTHS, "Month is a three-letter month name"
    assert 1900 <= year <= 2100, "Year is in the range [1900, 2100]"
    try:
        datetime.date(year, _MONTHS.index(month) + 1, day)
    except ValueError:
        raise AssertionError("the given dates are guaranteed to be valid") from None
