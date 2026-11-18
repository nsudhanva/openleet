"""Split Array with Equal Sum: an integer array."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 2000, "1 <= n <= 2000"
    assert all(-(10**6) <= v <= 10**6 for v in nums), "-10^6 <= nums[i] <= 10^6"
