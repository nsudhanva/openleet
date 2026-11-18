"""Peak Index in a Mountain Array: a mountain array of integers."""


def check(arr: list[int]) -> None:
    assert isinstance(arr, list), "arr is an array"
    assert 3 <= len(arr) <= 10**5, "3 <= arr.length <= 10^5"
    assert all(isinstance(v, int) and 0 <= v <= 10**6 for v in arr), "0 <= arr[i] <= 10^6"
    i = 0
    while i + 1 < len(arr) and arr[i] < arr[i + 1]:
        i += 1
    assert 0 < i < len(arr) - 1, "arr is guaranteed to be a mountain array"
    while i + 1 < len(arr) and arr[i] > arr[i + 1]:
        i += 1
    assert i == len(arr) - 1, "arr is guaranteed to be a mountain array"
