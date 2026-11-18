"""Valid Subarrays With Matching Sum Digits I: an integer array and a digit x."""


def check(nums: list[int], x: int) -> None:
    assert 1 <= len(nums) <= 1500, "1 <= nums.length <= 1500"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= x <= 9, "1 <= x <= 9"
