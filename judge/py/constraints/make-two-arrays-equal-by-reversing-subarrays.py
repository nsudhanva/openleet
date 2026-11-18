"""Make Two Arrays Equal by Reversing Subarrays: two equal-length arrays of 1..1000."""


def check(target: list[int], arr: list[int]) -> None:
    assert len(target) == len(arr), "target.length == arr.length"
    assert 1 <= len(target) <= 1000, "1 <= target.length <= 1000"
    assert all(1 <= v <= 1000 for v in target), "1 <= target[i] <= 1000"
    assert all(1 <= v <= 1000 for v in arr), "1 <= arr[i] <= 1000"
