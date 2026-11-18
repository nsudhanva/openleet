"""Binary Subarrays With Sum: a binary list and a goal."""


def check(nums: list[int], goal: int) -> None:
    assert isinstance(goal, int), "goal is an integer"
    assert 1 <= len(nums) <= 3 * 10**4, "1 <= nums.length <= 3 * 10^4"
    assert all(v in (0, 1) for v in nums), "nums[i] is either 0 or 1"
    assert 0 <= goal <= len(nums), "0 <= goal <= nums.length"
