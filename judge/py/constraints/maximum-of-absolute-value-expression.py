"""Maximum of Absolute Value Expression: two integer arrays of equal length."""


def check(arr1: list[int], arr2: list[int]) -> None:
    assert 2 <= len(arr1) == len(arr2) <= 40000, "2 <= arr1.length == arr2.length <= 40000"
    assert all(-(10**6) <= v <= 10**6 for v in arr1), "-10^6 <= arr1[i] <= 10^6"
    assert all(-(10**6) <= v <= 10**6 for v in arr2), "-10^6 <= arr2[i] <= 10^6"
