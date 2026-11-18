"""Sum of Even Numbers After Queries: an integer array and [val, index] queries."""


def check(nums: list[int], queries: list[list[int]]) -> None:
    assert 1 <= len(nums) <= 10**4, "1 <= nums.length <= 10^4"
    assert all(-(10**4) <= x <= 10**4 for x in nums), "-10^4 <= nums[i] <= 10^4"
    assert 1 <= len(queries) <= 10**4, "1 <= queries.length <= 10^4"
    assert all(len(q) == 2 for q in queries), "queries[i] = [val, index]"
    assert all(-(10**4) <= v <= 10**4 for v, _ in queries), "-10^4 <= vali <= 10^4"
    assert all(0 <= i < len(nums) for _, i in queries), "0 <= indexi < nums.length"
