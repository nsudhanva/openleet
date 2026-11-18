"""Letter Combinations of a Phone Number: a string of digits 2 to 9."""


def check(digits: str) -> None:
    assert 1 <= len(digits) <= 4, "1 <= digits.length <= 4"
    assert all("2" <= c <= "9" for c in digits), "digits[i] is a digit in the range ['2', '9']"
