"""Transform Array to All Equal Elements: an array of -1/1 and an operation limit k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(x in (-1, 1) for x in nums), "nums[i] is either -1 or 1"
    assert 1 <= k <= n, "1 <= k <= n"
