"""Binary Trees With Factors: distinct integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 1000, "1 <= arr.length <= 1000"
    assert all(2 <= v <= 10**9 for v in arr), "2 <= arr[i] <= 10^9"
    assert len(set(arr)) == len(arr), "all values of arr are unique"
