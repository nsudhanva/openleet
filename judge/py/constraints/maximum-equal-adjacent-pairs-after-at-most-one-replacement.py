"""Maximum Equal Adjacent Pairs After at Most One Replacement: an integer array."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 10**5, "2 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
