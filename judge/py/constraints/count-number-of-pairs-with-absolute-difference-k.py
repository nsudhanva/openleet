"""Count Number of Pairs With Absolute Difference K: a small integer array and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 200, "1 <= nums.length <= 200"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
    assert 1 <= k <= 99, "1 <= k <= 99"
