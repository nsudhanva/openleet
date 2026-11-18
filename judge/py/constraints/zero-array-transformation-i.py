"""Zero Array Transformation I: an array and [l, r] range queries."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= a <= b < n for a, b in queries), "0 <= li <= ri < nums.length"
