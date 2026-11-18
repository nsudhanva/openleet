"""Count the Digits That Divide a Number: an integer without zero digits."""


def check(num: int) -> None:
    assert 1 <= num <= 10**9, "1 <= num <= 10^9"
    assert "0" not in str(num), "num does not contain 0 as one of its digits"
