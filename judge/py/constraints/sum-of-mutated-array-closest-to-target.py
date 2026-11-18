"""Sum of Mutated Array Closest to Target: an integer array and a target."""


def check(arr: list[int], target: int) -> None:
    assert 1 <= len(arr) <= 10**4, "1 <= arr.length <= 10^4"
    assert all(1 <= v <= 10**5 for v in arr), "1 <= arr[i] <= 10^5"
    assert 1 <= target <= 10**5, "1 <= target <= 10^5"
