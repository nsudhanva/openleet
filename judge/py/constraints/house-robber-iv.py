"""House Robber IV: money in a row of houses and a number of houses to rob."""


def check(nums: list[int], k: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= x <= 10**9 for x in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= k <= (len(nums) + 1) // 2, "1 <= k <= (nums.length + 1)/2"
