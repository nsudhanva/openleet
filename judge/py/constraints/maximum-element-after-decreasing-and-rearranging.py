"""Maximum Element After Decreasing and Rearranging: an array of positive integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in arr), "1 <= arr[i] <= 10^9"
