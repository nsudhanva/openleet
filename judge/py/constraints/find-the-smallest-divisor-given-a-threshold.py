"""Find the Smallest Divisor Given a Threshold: an array and a threshold."""


def check(nums: list[int], threshold: int) -> None:
    assert 1 <= len(nums) <= 5 * 10**4, "1 <= nums.length <= 5 * 10^4"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert len(nums) <= threshold <= 10**6, "nums.length <= threshold <= 10^6"
