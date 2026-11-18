"""Count Ways To Build Good Strings: length bounds low, high and append sizes zero, one."""


def check(low: int, high: int, zero: int, one: int) -> None:
    assert 1 <= low <= high <= 10**5, "1 <= low <= high <= 10^5"
    assert 1 <= zero <= low, "1 <= zero <= low"
    assert 1 <= one <= low, "1 <= one <= low"
