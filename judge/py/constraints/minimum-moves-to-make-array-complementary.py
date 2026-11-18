"""Minimum Moves to Make Array Complementary: an even-length array and a limit."""


def check(nums: list[int], limit: int) -> None:
    n = len(nums)
    assert 2 <= n <= 10**5, "2 <= n == nums.length <= 10^5"
    assert n % 2 == 0, "n is even"
    assert 1 <= limit <= 10**5, "limit <= 10^5"
    assert all(1 <= v <= limit for v in nums), "1 <= nums[i] <= limit"
