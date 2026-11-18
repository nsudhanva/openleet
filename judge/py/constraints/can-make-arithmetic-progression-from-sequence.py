"""Can Make Arithmetic Progression From Sequence: an integer array."""


def check(arr: list[int]) -> None:
    assert 2 <= len(arr) <= 1000, "2 <= arr.length <= 1000"
    assert all(-(10**6) <= v <= 10**6 for v in arr), "-10^6 <= arr[i] <= 10^6"
