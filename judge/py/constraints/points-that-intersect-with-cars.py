"""Points That Intersect With Cars: car intervals [start, end]."""


def check(nums: list[list[int]]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(len(p) == 2 for p in nums), "nums[i].length == 2"
    assert all(1 <= s <= e <= 100 for s, e in nums), "1 <= starti <= endi <= 100"
