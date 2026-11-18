"""Find the Middle Index in Array: a short array of integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(-1000 <= v <= 1000 for v in nums), "-1000 <= nums[i] <= 1000"
