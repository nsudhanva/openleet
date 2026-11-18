"""Find K-th Smallest Pair Distance: an integer array and a rank k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
    assert all(0 <= v <= 10**6 for v in nums), "0 <= nums[i] <= 10^6"
    assert 1 <= k <= n * (n - 1) // 2, "1 <= k <= n * (n - 1) / 2"
