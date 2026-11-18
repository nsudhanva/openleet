"""Find Lucky Integer in an Array: a list of positive integers."""


def check(arr: list[int]) -> None:
    assert 1 <= len(arr) <= 500, "1 <= arr.length <= 500"
    assert all(1 <= v <= 500 for v in arr), "1 <= arr[i] <= 500"
