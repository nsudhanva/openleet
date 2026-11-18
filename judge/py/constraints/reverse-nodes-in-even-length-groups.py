"""Reverse Nodes in Even Length Groups: a linked list given as a list of values."""


def check(head: list[int]) -> None:
    assert 1 <= len(head) <= 10**5, "number of nodes is in [1, 10^5]"
    assert all(0 <= v <= 10**5 for v in head), "0 <= Node.val <= 10^5"
