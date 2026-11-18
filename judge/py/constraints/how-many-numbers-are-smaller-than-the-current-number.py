"""How Many Numbers Are Smaller Than the Current Number: a list of small integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 500, "2 <= nums.length <= 500"
    assert all(0 <= x <= 100 for x in nums), "0 <= nums[i] <= 100"
