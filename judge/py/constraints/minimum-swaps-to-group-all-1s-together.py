"""Minimum Swaps to Group All 1's Together: a binary array."""


def check(data: list[int]) -> None:
    assert 1 <= len(data) <= 10**5, "1 <= data.length <= 10^5"
    assert all(v in (0, 1) for v in data), "data[i] is either 0 or 1"
