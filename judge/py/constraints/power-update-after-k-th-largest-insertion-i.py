"""Power Update After K-th Largest Insertion I: nums, a base p and [val, k] queries."""


def check(nums: list[int], p: int, queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 2 * 10**4, "1 <= nums.length <= 2 * 10^4"
    assert all(1 <= v <= 10**6 for v in nums), "1 <= nums[i] <= 10^6"
    assert 1 <= p <= 10**6, "1 <= p <= 10^6"
    assert 1 <= len(queries) <= 2 * 10**4, "1 <= queries.length <= 2 * 10^4"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(1 <= val <= 10**6 for val, _ in queries), "1 <= vali <= 10^6"
    assert all(1 <= k <= n + i + 1 for i, (_, k) in enumerate(queries)), "1 <= ki <= n + i + 1"
    assert all(abs(queries[i][1] - queries[i - 1][1]) < 10 for i in range(1, len(queries))), (
        "|ki - ki-1| < 10 for i > 0"
    )
