"""Maximum Sum of Subsequence With Non-adjacent Elements: an array and point-update queries."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 5 * 10**4, "1 <= nums.length <= 5 * 10^4"
    assert all(-(10**5) <= v <= 10**5 for v in nums), "-10^5 <= nums[i] <= 10^5"
    assert 1 <= len(queries) <= 5 * 10**4, "1 <= queries.length <= 5 * 10^4"
    assert all(len(q) == 2 for q in queries), "queries[i] == [posi, xi]"
    assert all(0 <= p <= n - 1 for p, _ in queries), "0 <= posi <= nums.length - 1"
    assert all(-(10**5) <= x <= 10**5 for _, x in queries), "-10^5 <= xi <= 10^5"
