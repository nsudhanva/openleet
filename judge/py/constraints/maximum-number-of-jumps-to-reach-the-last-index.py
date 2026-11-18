"""Maximum Number of Jumps to Reach the Last Index: an integer array and a target."""


def check(nums: list[int], target: int) -> None:
    assert 2 <= len(nums) <= 1000, "2 <= nums.length == n <= 1000"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert 0 <= target <= 2 * 10**9, "0 <= target <= 2 * 10^9"
