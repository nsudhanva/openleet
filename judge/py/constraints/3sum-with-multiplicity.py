"""3Sum With Multiplicity: a list of small non-negative integers and a target."""


def check(arr: list[int], target: int) -> None:
    assert 3 <= len(arr) <= 3000, "3 <= arr.length <= 3000"
    assert all(0 <= x <= 100 for x in arr), "0 <= arr[i] <= 100"
    assert 0 <= target <= 300, "0 <= target <= 300"
