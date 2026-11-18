"""Count the Number of Fair Pairs: an integer array with lower and upper."""


def check(nums: list[int], lower: int, upper: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert -(10**9) <= lower <= upper <= 10**9, "-10^9 <= lower <= upper <= 10^9"
