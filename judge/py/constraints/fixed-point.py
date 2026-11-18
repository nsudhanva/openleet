"""Fixed Point: a sorted array of distinct integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) < 10**4, "1 <= arr.length < 10^4"
    assert all(-(10**9) <= v <= 10**9 for v in arr), "-10^9 <= arr[i] <= 10^9"
    assert all(arr[i] < arr[i + 1] for i in range(len(arr) - 1)), (
        "arr is distinct and sorted in ascending order"
    )
