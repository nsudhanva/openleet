"""Count Pairs Whose Sum is Less than Target: a small integer array and a target."""


def check(nums: list[int], target: int) -> None:
    assert 1 <= len(nums) <= 50, "1 <= nums.length == n <= 50"
    assert all(-50 <= v <= 50 for v in nums), "-50 <= nums[i] <= 50"
    assert -50 <= target <= 50, "-50 <= target <= 50"
