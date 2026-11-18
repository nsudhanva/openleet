"""Maximum Bitwise AND After Increment Operations: an array, k increments and m elements."""


def check(nums: list[int], k: int, m: int) -> None:
    n = len(nums)
    assert 1 <= n <= 5 * 10**4, "1 <= n == nums.length <= 5 * 10^4"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
    assert 1 <= m <= n, "1 <= m <= n"
