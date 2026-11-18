"""Minimum Time Difference: a list of "HH:MM" clock times."""


def check(timePoints: list[str]) -> None:
    assert 2 <= len(timePoints) <= 2 * 10**4, "2 <= timePoints.length <= 2 * 10^4"
    for t in timePoints:
        assert len(t) == 5 and t[2] == ":", 'timePoints[i] is in the format "HH:MM"'
        assert t[:2].isdigit() and t[3:].isdigit(), 'timePoints[i] is in the format "HH:MM"'
        assert t.isascii(), 'timePoints[i] is in the format "HH:MM"'
        assert int(t[:2]) <= 23 and int(t[3:]) <= 59, "valid 24-hour time"
