"""Maximum Strength of K Disjoint Subarrays: an integer array and an odd count k."""


def check(nums: list[int], k: int) -> None:
    n = len(nums)
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert all(-(10**9) <= v <= 10**9 for v in nums), "-10^9 <= nums[i] <= 10^9"
    assert 1 <= k <= n, "1 <= k <= n"
    assert 1 <= n * k <= 10**6, "1 <= n * k <= 10^6"
    assert k % 2 == 1, "k is odd"
