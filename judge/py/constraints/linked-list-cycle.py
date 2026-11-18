"""Linked List Cycle: a linked list and the index its tail links back to (-1 for none)."""


def check(head: list[int], pos: int = -1) -> None:
    n = len(head)
    assert 0 <= n <= 10**4, "number of nodes is in the range [0, 10^4]"
    assert all(-(10**5) <= v <= 10**5 for v in head), "-10^5 <= Node.val <= 10^5"
    assert pos == -1 or 0 <= pos < n, "pos is -1 or a valid index in the linked-list"
