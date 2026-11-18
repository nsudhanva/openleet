"""Make Array Zero by Subtracting Equal Amounts: an array of 0..100."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(0 <= v <= 100 for v in nums), "0 <= nums[i] <= 100"
