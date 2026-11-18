"""Contains Duplicate III: a list of integers with an index and a value difference."""


def check(nums: list[int], indexDiff: int, valueDiff: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(isinstance(v, int) for v in nums), "nums[i] is an integer"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert isinstance(indexDiff, int), "indexDiff is an integer"
    assert 1 <= indexDiff <= len(nums), "1 <= indexDiff <= nums.length"
    assert isinstance(valueDiff, int), "valueDiff is an integer"
    assert 0 <= valueDiff <= 10**9, "0 <= valueDiff <= 10^9"
