"""Plus One: the digits of a non-negative integer, most significant first."""


def check(digits: list[int]) -> None:
    assert 1 <= len(digits) <= 100, "1 <= digits.length <= 100"
    assert all(0 <= d <= 9 for d in digits), "0 <= digits[i] <= 9"
    assert digits[0] != 0 or len(digits) == 1, "digits does not contain any leading 0's"
