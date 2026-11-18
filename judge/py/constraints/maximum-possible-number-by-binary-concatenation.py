"""Maximum Possible Number by Binary Concatenation: an array of three integers."""


def check(nums: list[int]) -> None:
    assert len(nums) == 3, "nums.length == 3"
    assert all(1 <= v <= 127 for v in nums), "1 <= nums[i] <= 127"
