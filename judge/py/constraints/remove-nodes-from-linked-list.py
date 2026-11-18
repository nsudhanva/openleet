"""Remove Nodes From Linked List: a non-empty linked list of positive values."""


def check(head: list[int]) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert 1 <= len(head) <= 10**5, "number of nodes in [1, 10^5]"
    assert all(1 <= v <= 10**5 for v in head), "1 <= Node.val <= 10^5"
