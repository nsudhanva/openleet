"""Reorder List: a non-empty linked list of values."""


def check(head: list[int]) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert 1 <= len(head) <= 5 * 10**4, "number of nodes in [1, 5 * 10^4]"
    assert all(1 <= v <= 1000 for v in head), "1 <= Node.val <= 1000"
