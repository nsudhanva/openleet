"""Zero Array Transformation III: an array and queries [l, r]."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= q[0] <= q[1] < n for q in queries), "0 <= li <= ri < nums.length"
