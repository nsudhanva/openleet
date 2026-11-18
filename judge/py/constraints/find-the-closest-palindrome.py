"""Find the Closest Palindrome: a positive integer as a decimal string."""


def check(n: str) -> None:
    assert isinstance(n, str), "n is a string"
    assert 1 <= len(n) <= 18, "1 <= n.length <= 18"
    assert n.isascii() and n.isdigit(), "n consists of only digits"
    assert n[0] != "0", "n does not have leading zeros"
    assert 1 <= int(n) <= 10**18 - 1, "n is in the range [1, 10^18 - 1]"
