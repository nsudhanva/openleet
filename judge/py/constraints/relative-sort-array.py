"""Relative Sort Array: arr1 and a list arr2 of distinct values that all occur in arr1."""


def check(arr1: list[int], arr2: list[int]) -> None:
    assert 1 <= len(arr1) <= 1000, "1 <= arr1.length <= 1000"
    assert 1 <= len(arr2) <= 1000, "1 <= arr2.length <= 1000"
    assert all(0 <= v <= 1000 for v in arr1 + arr2), "0 <= arr1[i], arr2[i] <= 1000"
    assert len(set(arr2)) == len(arr2), "all the elements of arr2 are distinct"
    assert set(arr2) <= set(arr1), "each arr2[i] is in arr1"
