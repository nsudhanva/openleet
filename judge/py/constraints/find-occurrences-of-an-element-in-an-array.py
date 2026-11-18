"""Find Occurrences of an Element in an Array: nums, occurrence queries and a value x."""


def check(nums: list[int], queries: list[int], x: int) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert 1 <= len(queries) <= 10**5, "1 <= queries.length <= 10^5"
    assert all(1 <= q <= 10**5 for q in queries), "1 <= queries[i] <= 10^5"
    assert all(1 <= v <= 10**4 for v in nums), "1 <= nums[i] <= 10^4"
    assert 1 <= x <= 10**4, "1 <= x <= 10^4"
