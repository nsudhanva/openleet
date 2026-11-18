"""Remove Digit From Number to Maximize Result: a digit string and a digit that occurs in it."""


def check(number: str, digit: str) -> None:
    assert 2 <= len(number) <= 100, "2 <= number.length <= 100"
    assert all("1" <= c <= "9" for c in number), "number consists of digits from '1' to '9'"
    assert len(digit) == 1 and "1" <= digit <= "9", "digit is a digit from '1' to '9'"
    assert digit in number, "digit occurs at least once in number"
