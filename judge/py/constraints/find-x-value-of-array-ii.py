"""Find X Value of Array II: an array of positive ints, a modulus k and update queries."""


def check(nums: list[int], k: int, queries: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**9 for v in nums), "1 <= nums[i] <= 10^9"
    assert 1 <= k <= 5, "1 <= k <= 5"
    assert 1 <= len(queries) <= 2 * 10**4, "1 <= queries.length <= 2 * 10^4"
    assert all(len(q) == 4 for q in queries), "queries[i] == [indexi, valuei, starti, xi]"
    assert all(0 <= q[0] <= n - 1 for q in queries), "0 <= indexi <= nums.length - 1"
    assert all(1 <= q[1] <= 10**9 for q in queries), "1 <= valuei <= 10^9"
    assert all(0 <= q[2] <= n - 1 for q in queries), "0 <= starti <= nums.length - 1"
    assert all(0 <= q[3] <= k - 1 for q in queries), "0 <= xi <= k - 1"
