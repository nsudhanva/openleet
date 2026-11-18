"""Number of Divisible Triplet Sums: an array of positive integers and a divisor."""


def check(nums: list[int], d: int) -> None:
    assert 1 <= len(nums) <= 1000, "1 <= nums.length <= 1000"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= d <= 10**9, "1 <= d <= 10^9"
