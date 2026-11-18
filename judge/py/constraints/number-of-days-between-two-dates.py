"""Number of Days Between Two Dates: two YYYY-MM-DD date strings."""

from datetime import date


def _valid(d: str) -> bool:
    if len(d) != 10 or d[4] != "-" or d[7] != "-":
        return False
    if not (d[:4] + d[5:7] + d[8:]).isdigit() or not d.isascii():
        return False
    try:
        date(int(d[:4]), int(d[5:7]), int(d[8:]))
    except ValueError:
        return False
    return 1971 <= int(d[:4]) <= 2100


def check(date1: str, date2: str) -> None:
    assert isinstance(date1, str) and _valid(date1), (
        "date1 is a valid YYYY-MM-DD date between the years 1971 and 2100"
    )
    assert isinstance(date2, str) and _valid(date2), (
        "date2 is a valid YYYY-MM-DD date between the years 1971 and 2100"
    )
