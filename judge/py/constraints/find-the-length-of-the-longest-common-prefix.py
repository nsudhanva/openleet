"""Find the Length of the Longest Common Prefix: two arrays of positive integers."""


def check(arr1: list[int], arr2: list[int]) -> None:
    assert isinstance(arr1, list) and isinstance(arr2, list), "arr1 and arr2 are arrays"
    assert 1 <= len(arr1) <= 5 * 10**4, "1 <= arr1.length <= 5 * 10^4"
    assert 1 <= len(arr2) <= 5 * 10**4, "1 <= arr2.length <= 5 * 10^4"
    assert all(1 <= v <= 10**8 for v in arr1), "1 <= arr1[i] <= 10^8"
    assert all(1 <= v <= 10**8 for v in arr2), "1 <= arr2[i] <= 10^8"
