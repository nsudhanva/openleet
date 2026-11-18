"""Largest Time for Given Digits: four decimal digits."""


def check(arr: list[int]) -> None:
    assert len(arr) == 4, "arr.length == 4"
    assert all(0 <= d <= 9 for d in arr), "0 <= arr[i] <= 9"
