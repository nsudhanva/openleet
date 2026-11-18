"""Special Array II: a list of integers and inclusive [from, to] subarray queries."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= q[0] <= q[1] <= n - 1 for q in queries), (
        "0 <= queries[i][0] <= queries[i][1] <= nums.length - 1"
    )
