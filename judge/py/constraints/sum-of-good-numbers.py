"""Sum of Good Numbers: an integer array and a distance k."""


def check(nums: list[int], k: int) -> None:
    assert 2 <= len(nums) <= 100, "2 <= nums.length <= 100"
    assert all(1 <= x <= 1000 for x in nums), "1 <= nums[i] <= 1000"
    assert 1 <= k <= len(nums) // 2, "1 <= k <= floor(nums.length / 2)"
