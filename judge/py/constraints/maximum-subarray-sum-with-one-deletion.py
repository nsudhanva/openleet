"""Maximum Subarray Sum with One Deletion: an integer array."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(-(10**4) <= v <= 10**4 for v in arr), "-10^4 <= arr[i] <= 10^4"
