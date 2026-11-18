"""Check If N and Its Double Exist: an integer array."""


def check(arr: list[int]) -> None:
    assert 2 <= len(arr) <= 500, "2 <= arr.length <= 500"
    assert all(-(10**3) <= v <= 10**3 for v in arr), "-10^3 <= arr[i] <= 10^3"
