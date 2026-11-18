"""Type of Triangle: three side lengths."""


def check(nums: list[int]) -> None:
    assert len(nums) == 3, "nums.length == 3"
    assert all(1 <= v <= 100 for v in nums), "1 <= nums[i] <= 100"
