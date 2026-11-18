"""Insertion Sort List: a linked list of values."""


def check(head: list[int]) -> None:
    assert isinstance(head, list), "head is a list"
    assert 1 <= len(head) <= 5000, "number of nodes in [1, 5000]"
    assert all(-5000 <= v <= 5000 for v in head), "-5000 <= Node.val <= 5000"
