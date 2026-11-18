"""Query Kth Smallest Trimmed Number: equal-length digit strings and (k, trim) queries."""


def check(nums: list[str], queries: list[list[int]]) -> None:
    assert isinstance(nums, list) and isinstance(queries, list), "nums and queries are arrays"
    assert 1 <= len(nums) <= 100, "1 <= nums.length <= 100"
    assert all(isinstance(s, str) for s in nums), "nums[i] is a string"
    size = len(nums[0])
    assert 1 <= size <= 100, "1 <= nums[i].length <= 100"
    assert all(len(s) == size for s in nums), "all nums[i].length are equal"
    assert all(s.isascii() and s.isdigit() for s in nums), "nums[i] consists of only digits"
    assert 1 <= len(queries) <= 100, "1 <= queries.length <= 100"
    assert all(isinstance(q, list) and len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(1 <= k <= len(nums) for k, _ in queries), "1 <= ki <= nums.length"
    assert all(1 <= t <= size for _, t in queries), "1 <= trimi <= nums[i].length"
