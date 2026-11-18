"""Maximum Value after Insertion: a digit string (maybe negative) and a digit x."""


def check(n: str, x: int) -> None:
    assert 1 <= len(n) <= 10**5, "1 <= n.length <= 10^5"
    assert 1 <= x <= 9, "1 <= x <= 9"
    digits = n[1:] if n.startswith("-") else n
    assert len(digits) >= 1, "n is a valid representation of an integer"
    assert all(c in "123456789" for c in digits), "the digits in n are in the range [1, 9]"
