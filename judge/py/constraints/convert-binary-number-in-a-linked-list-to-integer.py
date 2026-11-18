"""Convert Binary Number in a Linked List to Integer: a list of bits."""


def check(head: list[int]) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert 1 <= len(head) <= 30, "The Linked List is not empty and has at most 30 nodes"
    assert all(v in (0, 1) for v in head), "Each node's value is either 0 or 1"
