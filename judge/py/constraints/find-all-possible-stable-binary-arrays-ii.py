"""Find All Possible Stable Binary Arrays II: counts of zeros and ones and a run limit."""


def check(zero: int, one: int, limit: int) -> None:
    assert 1 <= zero <= 1000, "1 <= zero <= 1000"
    assert 1 <= one <= 1000, "1 <= one <= 1000"
    assert 1 <= limit <= 1000, "1 <= limit <= 1000"
