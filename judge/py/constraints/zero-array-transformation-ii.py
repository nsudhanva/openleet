"""Zero Array Transformation II: an array and queries [l, r, val]."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(0 <= v <= 5 * 10**5 for v in nums), "0 <= nums[i] <= 5 * 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 3 for q in queries), "queries[i].length == 3"
    assert all(0 <= q[0] <= q[1] < n for q in queries), "0 <= li <= ri < nums.length"
    assert all(1 <= q[2] <= 5 for q in queries), "1 <= vali <= 5"
