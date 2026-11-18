"""Remove Duplicates from Sorted List: a linked list sorted in ascending order."""

from itertools import pairwise


def check(head: list[int]) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert 0 <= len(head) <= 300, "number of nodes in [0, 300]"
    assert all(-100 <= v <= 100 for v in head), "-100 <= Node.val <= 100"
    assert all(a <= b for a, b in pairwise(head)), "list sorted in ascending order"
