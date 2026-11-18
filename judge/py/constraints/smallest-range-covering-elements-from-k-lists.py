"""Smallest Range Covering Elements from K Lists: k sorted lists of integers."""


def check(nums: list[list[int]]) -> None:
    assert 1 <= len(nums) <= 3500, "1 <= k <= 3500"
    assert all(1 <= len(r) <= 50 for r in nums), "1 <= nums[i].length <= 50"
    assert all(-(10**5) <= v <= 10**5 for r in nums for v in r), "-10^5 <= nums[i][j] <= 10^5"
    assert all(r[i] <= r[i + 1] for r in nums for i in range(len(r) - 1)), (
        "nums[i] is sorted in non-decreasing order"
    )
