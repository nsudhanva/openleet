"""Maximum Width Ramp: an array of non-negative ints."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 5 * 10**4, "2 <= nums.length <= 5 * 10^4"
    assert all(0 <= v <= 5 * 10**4 for v in nums), "0 <= nums[i] <= 5 * 10^4"
