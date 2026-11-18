"""Reverse Linked List: a linked list given as a list of values."""


def check(head: list[int]) -> None:
    assert 0 <= len(head) <= 5000, "number of nodes is in [0, 5000]"
    assert all(-5000 <= v <= 5000 for v in head), "-5000 <= Node.val <= 5000"
