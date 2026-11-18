"""Find Minimum Cost to Remove Array Elements: a list of positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
