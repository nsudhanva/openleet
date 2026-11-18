"""Max Consecutive Ones II: a binary array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(v in (0, 1) for v in nums), "nums[i] is either 0 or 1"
