"""Maximum Sum Obtained of Any Permutation: an integer array and inclusive index ranges."""


def check(nums: list[int], requests: list[list[int]]) -> None:
    n = len(nums)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(0 <= v <= 10**5 for v in nums), "0 <= nums[i] <= 10^5"
    assert 1 <= len(requests) <= 10**5, "1 <= requests.length <= 10^5"
    assert all(len(r) == 2 for r in requests), "requests[i].length == 2"
    assert all(0 <= s <= e < n for s, e in requests), "0 <= starti <= endi < n"
