"""Total Hamming Distance: an array of non-negative integers."""


def check(nums: list[int]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**4, "1 <= nums.length <= 10^4"
    assert all(0 <= x <= 10**9 for x in nums), "0 <= nums[i] <= 10^9"
    total = 0
    for b in range(30):
        ones = sum((x >> b) & 1 for x in nums)
        total += ones * (n - ones)
    assert total <= 2**31 - 1, "the answer fits in a 32-bit integer"
