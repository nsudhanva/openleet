"""Maximum XOR With an Element From Array: an integer array and [x, m] queries."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= v <= 10**9 for v in nums), "0 <= nums[j] <= 10^9"
    assert all(0 <= v <= 10**9 for q in queries for v in q), "0 <= xi, mi <= 10^9"
