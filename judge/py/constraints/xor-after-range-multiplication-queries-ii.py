"""XOR After Range Multiplication Queries II: an array and [l, r, k, v] queries."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n == nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= len(queries) <= 10**5, "1 <= q == queries.length <= 10^5"
    assert all(len(qr) == 4 for qr in queries), "queries[i] = [li, ri, ki, vi]"
    assert all(0 <= lo <= hi < n for lo, hi, _, _ in queries), "0 <= li <= ri < n"
    assert all(1 <= k <= n for _, _, k, _ in queries), "1 <= ki <= n"
    assert all(1 <= v <= 10**5 for _, _, _, v in queries), "1 <= vi <= 10^5"
