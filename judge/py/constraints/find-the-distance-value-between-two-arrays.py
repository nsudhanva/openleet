"""Find the Distance Value Between Two Arrays: two integer arrays and a distance d."""


def check(arr1: list[int], arr2: list[int], d: int) -> None:
    assert isinstance(arr1, list) and isinstance(arr2, list), "arr1 and arr2 are arrays"
    assert 1 <= len(arr1) <= 500, "1 <= arr1.length <= 500"
    assert 1 <= len(arr2) <= 500, "1 <= arr2.length <= 500"
    assert all(-1000 <= v <= 1000 for v in arr1), "-1000 <= arr1[i] <= 1000"
    assert all(-1000 <= v <= 1000 for v in arr2), "-1000 <= arr2[j] <= 1000"
    assert 0 <= d <= 100, "0 <= d <= 100"
