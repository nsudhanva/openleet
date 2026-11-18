"""Find K Closest Elements: a sorted array, a count k and a target x."""


def check(arr: list[int], k: int, x: int) -> None:
    assert 1 <= len(arr) <= 10**4, "1 <= arr.length <= 10^4"
    assert 1 <= k <= len(arr), "1 <= k <= arr.length"
    assert all(-(10**4) <= v <= 10**4 for v in arr), "-10^4 <= arr[i] <= 10^4"
    assert -(10**4) <= x <= 10**4, "-10^4 <= x <= 10^4"
    assert all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)), (
        "arr is sorted in ascending order"
    )
