"""Mean of Array After Removing Some Elements: an integer array whose length is a multiple of 20."""


def check(arr: list[int]) -> None:
    assert 20 <= len(arr) <= 1000, "20 <= arr.length <= 1000"
    assert len(arr) % 20 == 0, "arr.length is a multiple of 20"
    assert all(0 <= v <= 10**5 for v in arr), "0 <= arr[i] <= 10^5"
