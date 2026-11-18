"""Maximum 69 Number: a positive integer made only of the digits 6 and 9."""


def check(num: int) -> None:
    assert 1 <= num <= 10**4, "1 <= num <= 10^4"
    assert set(str(num)) <= {"6", "9"}, "num consists of only 6 and 9 digits"
