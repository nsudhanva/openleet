"""Prime In Diagonal: a square matrix of positive integers."""


def check(nums: list[list[int]]) -> None:
    assert isinstance(nums, list) and all(isinstance(r, list) for r in nums), "nums is a matrix"
    assert 1 <= len(nums) <= 300, "1 <= nums.length <= 300"
    assert all(len(r) == len(nums) for r in nums), "nums.length == nums[i].length"
    assert all(1 <= v <= 4 * 10**6 for r in nums for v in r), "1 <= nums[i][j] <= 4 * 10^6"
