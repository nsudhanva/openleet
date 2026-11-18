"""Odd Even Linked List: a linked list given as a list of values."""


def check(head: list[int]) -> None:
    assert 0 <= len(head) <= 10**4, "number of nodes in [0, 10^4]"
    assert all(-(10**6) <= v <= 10**6 for v in head), "-10^6 <= Node.val <= 10^6"
