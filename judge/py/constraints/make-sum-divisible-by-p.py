"""Make Sum Divisible by P: an array of positive integers and a divisor p."""


def check(nums: list[int], p: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= p <= 10**9, "1 <= p <= 10^9"
