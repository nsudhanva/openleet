"""Array Partition: 2n integers."""


def check(nums: list[int]) -> None:
    assert len(nums) % 2 == 0, "nums.length == 2 * n"
    n = len(nums) // 2
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert all(-(10**4) <= v <= 10**4 for v in nums), "-10^4 <= nums[i] <= 10^4"
