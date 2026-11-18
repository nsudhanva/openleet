"""Smallest Good Base: an integer given as a decimal string."""


def check(n: str) -> None:
    assert isinstance(n, str) and n.isascii() and n.isdigit(), "n is an integer"
    assert n[0] != "0", "n does not contain any leading zeros"
    assert 3 <= int(n) <= 10**18, "n is in the range [3, 10^18]"
