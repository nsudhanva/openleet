"""Sort Array by Increasing Frequency: a list of small integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(isinstance(v, int) and -100 <= v <= 100 for v in nums), "-100 <= nums[i] <= 100"
