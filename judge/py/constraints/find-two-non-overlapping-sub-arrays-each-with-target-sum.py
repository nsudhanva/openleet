"""Find Two Non-overlapping Sub-arrays Each With Target Sum: positive integers and a target."""


def check(arr: list[int], target: int) -> None:
    assert 1 <= len(arr) <= 10**5, "1 <= arr.length <= 10^5"
    assert all(1 <= v <= 1000 for v in arr), "1 <= arr[i] <= 1000"
    assert 1 <= target <= 10**8, "1 <= target <= 10^8"
