"""Find All Possible Stable Binary Arrays I: counts of zeros and ones and a run limit."""


def check(zero: int, one: int, limit: int) -> None:
    assert 1 <= zero <= 200, "1 <= zero <= 200"
    assert 1 <= one <= 200, "1 <= one <= 200"
    assert 1 <= limit <= 200, "1 <= limit <= 200"
