"""Reverse Linked List II: a linked list given as a list of values and positions left, right."""


def check(head: list[int], left: int, right: int) -> None:
    n = len(head)
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(-500 <= v <= 500 for v in head), "-500 <= Node.val <= 500"
    assert 1 <= left <= right <= n, "1 <= left <= right <= n"
