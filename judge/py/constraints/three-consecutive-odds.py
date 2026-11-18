"""Three Consecutive Odds: an array of integers in [1, 1000]."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 1000, "1 <= arr.length <= 1000"
    assert all(1 <= x <= 1000 for x in arr), "1 <= arr[i] <= 1000"
