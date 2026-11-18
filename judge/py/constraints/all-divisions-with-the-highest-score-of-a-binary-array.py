"""All Divisions With the Highest Score of a Binary Array: a 0/1 array."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(v in (0, 1) for v in nums), "nums[i] is either 0 or 1"
