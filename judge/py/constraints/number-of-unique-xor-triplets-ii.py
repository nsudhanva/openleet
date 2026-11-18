"""Number of Unique XOR Triplets II: an array of integers up to 1500."""


def check(nums: list[int]) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 1500, "1 <= nums.length <= 1500"
    assert all(1 <= v <= 1500 for v in nums), "1 <= nums[i] <= 1500"
