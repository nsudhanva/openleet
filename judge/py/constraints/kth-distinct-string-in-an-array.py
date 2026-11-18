"""Kth Distinct String in an Array: lowercase strings and k."""


def check(arr: list[str], k: int) -> None:
    assert 1 <= len(arr) <= 1000, "1 <= arr.length <= 1000"
    assert 1 <= k <= len(arr), "1 <= k <= arr.length"
    assert all(1 <= len(s) <= 5 for s in arr), "1 <= arr[i].length <= 5"
    assert all(s.isascii() and s.isalpha() and s.islower() for s in arr), (
        "lowercase English letters"
    )
