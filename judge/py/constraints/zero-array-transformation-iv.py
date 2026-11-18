"""Zero Array Transformation IV: a short array and queries [l, r, val]."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10, "1 <= nums.length <= 10"
    assert all(0 <= v <= 1000 for v in nums), "0 <= nums[i] <= 1000"
    assert 1 <= len(queries) <= 1000, "1 <= queries.length <= 1000"
    assert all(len(q) == 3 for q in queries), "queries[i] = [li, ri, vali]"
    assert all(len(q) == 3 for q in queries), "queries[i] has 3 elements"
    assert all(0 <= q[0] <= q[1] < n for q in queries), "0 <= li <= ri < nums.length"
    assert all(1 <= q[2] <= 10 for q in queries), "1 <= vali <= 10"
