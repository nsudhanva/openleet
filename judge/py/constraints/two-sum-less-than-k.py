"""Two Sum Less Than K: an integer array and a bound k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(1 <= v <= 1000 for v in nums), "1 <= nums[i] <= 1000"
    assert 1 <= k <= 2000, "1 <= k <= 2000"
