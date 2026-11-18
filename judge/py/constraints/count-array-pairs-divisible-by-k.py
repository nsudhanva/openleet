"""Count Array Pairs Divisible by K: a list of integers and a divisor k."""


def check(nums: list[int], k: int) -> None:
    assert isinstance(nums, list), "nums is a list"
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(isinstance(v, int) for v in nums), "nums[i] is an integer"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert isinstance(k, int), "k is an integer"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
