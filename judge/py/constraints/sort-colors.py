"""Sort Colors: a list of 0s, 1s and 2s."""


def check(nums: list[int]) -> None:
    assert 1 <= len(nums) <= 300, "1 <= n <= 300"
    assert all(isinstance(v, int) and v in (0, 1, 2) for v in nums), "nums[i] is 0, 1, or 2"
