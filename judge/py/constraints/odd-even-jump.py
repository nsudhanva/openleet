"""Odd Even Jump: an integer array."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 2 * 10**4, "1 <= arr.length <= 2 * 10^4"
    assert all(0 <= v < 10**5 for v in arr), "0 <= arr[i] < 10^5"
