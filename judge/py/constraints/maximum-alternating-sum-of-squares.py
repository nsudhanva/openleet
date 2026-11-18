"""Maximum Alternating Sum of Squares: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-4 * 10**4 <= v <= 4 * 10**4 for v in nums), "-4 * 10^4 <= nums[i] <= 4 * 10^4"
