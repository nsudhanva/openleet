"""Intersection of Three Sorted Arrays: three strictly increasing integer arrays."""


def check(arr1: list[int], arr2: list[int], arr3: list[int]) -> None:
    for a in (arr1, arr2, arr3):
        assert isinstance(a, list), "arrays are lists"
        assert 1 <= len(a) <= 1000, "1 <= arr.length <= 1000"
        assert all(1 <= v <= 2000 for v in a), "1 <= arr[i] <= 2000"
        assert all(a[i] < a[i + 1] for i in range(len(a) - 1)), "arrays are strictly increasing"
