"""Finding 3-Digit Even Numbers: an array of digits."""


def check(digits: list[int]) -> None:
    assert 3 <= len(digits) <= 100, "3 <= digits.length <= 100"
    assert all(0 <= d <= 9 for d in digits), "0 <= digits[i] <= 9"
