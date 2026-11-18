"""Split Array into Consecutive Subsequences: a sorted integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
    assert all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1)), (
        "nums is sorted in non-decreasing order"
    )
