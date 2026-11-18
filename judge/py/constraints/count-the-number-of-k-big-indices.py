"""Count the Number of K-Big Indices: an array of positive integers and k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= n for v in nums), "1 <= nums[i] <= nums.length"
    assert 1 <= k <= n, "1 <= k <= nums.length"
