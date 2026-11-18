"""Swap Nodes in Pairs: a linked list given as a list of values."""


def check(head: list[int]) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert 0 <= len(head) <= 100, "number of nodes in [0, 100]"
    assert all(isinstance(v, int) and 0 <= v <= 100 for v in head), "0 <= Node.val <= 100"
