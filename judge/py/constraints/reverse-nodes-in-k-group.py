"""Reverse Nodes in k-Group: a linked list given as a list of values and a group size k."""


def check(head: list[int], k: int) -> None:
    n = len(head)
    assert 1 <= n <= 5000, "n <= 5000"
    assert 1 <= k <= n, "1 <= k <= n"
    assert all(0 <= v <= 1000 for v in head), "0 <= Node.val <= 1000"
