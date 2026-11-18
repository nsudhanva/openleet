"""Good Subsequence Queries: an integer array, a divisor p and point-update queries."""


def check(nums: list[int], p: int, queries: list[list[int]]) -> None:
    n = len(nums)
    assert 2 <= n <= 5 * 10**4, "2 <= n <= 5 * 10^4"
    assert all(1 <= v <= 5 * 10**4 for v in nums), "1 <= nums[i] <= 5 * 10^4"
    assert 1 <= len(queries) <= 5 * 10**4, "1 <= queries.length <= 5 * 10^4"
    assert all(len(q) == 2 for q in queries), "queries[i] = [indi, vali]"
    assert 1 <= p <= 5 * 10**4, "1 <= p <= 5 * 10^4"
    assert all(1 <= q[1] <= 5 * 10**4 for q in queries), "1 <= vali <= 5 * 10^4"
    assert all(0 <= q[0] <= n - 1 for q in queries), "0 <= indi <= n - 1"
