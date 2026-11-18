"""Search Insert Position: distinct ascending integers plus a target."""


def check(nums: list[int], target: int) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
    assert all(nums[i] < nums[i + 1] for i in range(len(nums) - 1)), (
        "nums contains distinct values sorted in ascending order"
    )
    assert -(10**4) <= target <= 10**4, "-10^4 <= target <= 10^4"
