"""Minimum Number of Operations to Convert Time: two 24-hour "HH:MM" times."""

import re


def _minutes(t: str) -> int:
    assert isinstance(t, str) and re.fullmatch(r"\d\d:\d\d", t), 'format "HH:MM"'
    h, m = int(t[:2]), int(t[3:])
    assert h <= 23 and m <= 59, "a valid 24-hour time"
    return h * 60 + m


def check(current: str, correct: str) -> None:
    a = _minutes(current)
    b = _minutes(correct)
    assert a <= b, "current <= correct"
