"""Adjacent Increasing Subarrays Detection I: a list of integers and a length k."""


def check(nums: list[int], k: int) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert 1 < 2 * k <= len(nums), "1 < 2 * k <= nums.length"
    assert all(-1000 <= x <= 1000 for x in nums), "-1000 <= nums[i] <= 1000"
