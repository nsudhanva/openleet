"""Count Number of Maximum Bitwise-OR Subsets: up to 16 positive integers."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 16, "1 <= nums.length <= 16"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
