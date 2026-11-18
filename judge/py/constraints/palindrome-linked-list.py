"""Palindrome Linked List: a linked list of digits, given as a list of values."""


def check(head: list[int]) -> None:
    assert isinstance(head, list), "the list is given as a list of values"
    assert 1 <= len(head) <= 10**5, "the number of nodes is in the range [1, 10^5]"
    assert all(0 <= v <= 9 for v in head), "0 <= Node.val <= 9"
