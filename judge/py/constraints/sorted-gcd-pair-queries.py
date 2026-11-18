"""Sorted GCD Pair Queries: a list of integers and pair-index queries."""


def check(nums: list[int], queries: list[int]) -> None:
    n = len(nums)
    assert 2 <= n <= 10**5, "2 <= n == nums.length <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 5 * 10**4 for v in nums), "1 <= nums[i] <= 5 * 10^4"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(isinstance(q, int) and 0 <= q < n * (n - 1) // 2 for q in queries), (
        "0 <= queries[i] < n * (n - 1) / 2"
    )
