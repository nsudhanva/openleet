"""Previous Permutation With One Swap: an array of positive integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 10**4, "1 <= arr.length <= 10^4"
    assert all(1 <= v <= 10**4 for v in arr), "1 <= arr[i] <= 10^4"
