"""Delete Nodes From Linked List Present in Array: unique values to remove, and a linked list."""


def check(nums: list[int], head: list[int]) -> None:
    assert 1 <= len(nums) <= 10**5, "1 <= nums.length <= 10^5"
    assert all(1 <= v <= 10**5 for v in nums), "1 <= nums[i] <= 10^5"
    assert len(set(nums)) == len(nums), "all elements in nums are unique"
    assert 1 <= len(head) <= 10**5, "the number of nodes is in the range [1, 10^5]"
    assert all(1 <= v <= 10**5 for v in head), "1 <= Node.val <= 10^5"
    banned = set(nums)
    assert any(v not in banned for v in head), "at least one node has a value not present in nums"
