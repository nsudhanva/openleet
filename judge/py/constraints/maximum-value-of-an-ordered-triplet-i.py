"""Maximum Value of an Ordered Triplet I: a short array of positive ints."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 100, "3 <= nums.length <= 100"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
