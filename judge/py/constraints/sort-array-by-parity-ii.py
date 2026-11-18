"""Sort Array By Parity II: a list with exactly half even integers."""


def check(nums: list[int]) -> None:
    assert 2 <= len(nums) <= 2 * 10**4, "2 <= nums.length <= 2 * 10^4"
    assert len(nums) % 2 == 0, "nums.length is even"
    assert all(isinstance(v, int) and 0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
    assert sum(v % 2 == 0 for v in nums) * 2 == len(nums), "half of the integers in nums are even"
