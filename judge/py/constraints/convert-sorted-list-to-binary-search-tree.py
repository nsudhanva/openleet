"""Convert Sorted List to Binary Search Tree: a linked list sorted in ascending order."""

from itertools import pairwise


def check(head: list[int]) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert 0 <= len(head) <= 2 * 10**4, "The number of nodes in head is in the range [0, 2 * 10^4]"
    assert all(isinstance(v, int) for v in head), "Node.val is an integer"
    assert all(-(10**5) <= v <= 10**5 for v in head), "-10^5 <= Node.val <= 10^5"
    assert all(a <= b for a, b in pairwise(head)), "head is sorted in ascending order"
