"""Apply Operations on Array to Maximize Sum of Squares: positive integers and k."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= k <= len(nums) <= 10**5, "1 <= k <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
