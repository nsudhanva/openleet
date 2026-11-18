"""Neighboring Bitwise XOR: a list of 0s and 1s."""


def check(derived: list[int]) -> None:
    assert 1 <= len(derived) <= 10**5, "1 <= n <= 10^5"
    assert all(v in (0, 1) for v in derived), "the values in derived are either 0's or 1's"
