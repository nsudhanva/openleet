"""Linked List Components: a linked list of unique values 0..n-1 and a unique subset of them."""


def check(head: list[int], nums: list[int]) -> None:
    n = len(head)
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert all(0 <= v < n for v in head), "0 <= Node.val < n"
    assert len(set(head)) == n, "all the values Node.val are unique"
    assert 1 <= len(nums) <= n, "1 <= nums.length <= n"
    assert all(0 <= v < n for v in nums), "0 <= nums[i] < n"
    assert len(set(nums)) == len(nums), "all the values of nums are unique"
