"""Partition Array Into Two Arrays to Minimize Sum Difference: an array of 2 * n integers."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is an array"
    assert len(nums) % 2 == 0, "nums.length == 2 * n"
    n = len(nums) // 2
    assert 1 <= n <= 15, "1 <= n <= 15"
    assert all(isinstance(v, int) and -(10**7) <= v <= 10**7 for v in nums), (
        "-10^7 <= nums[i] <= 10^7"
    )
