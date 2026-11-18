"""Array With Elements Not Equal to Average of Neighbors: an integer array."""


def check(nums: list[int]) -> None:
    assert 3 <= len(nums) <= 10**5, "3 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
