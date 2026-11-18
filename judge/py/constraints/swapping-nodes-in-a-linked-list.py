"""Swapping Nodes in a Linked List: a linked list of values and an index k."""


def check(head: list[int], k: int) -> None:
    assert isinstance(head, list), "head is a list of values"
    n = len(head)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert isinstance(k, int) and 1 <= k <= n, "1 <= k <= n"
    assert all(isinstance(v, int) and 0 <= v <= 100 for v in head), "0 <= Node.val <= 100"
