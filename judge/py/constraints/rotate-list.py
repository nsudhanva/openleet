"""Rotate List: a linked list of values and a rotation count."""


def check(head: list[int], k: int) -> None:
    assert len(head) <= 500, "the number of nodes in the list is in the range [0, 500]"
    assert all(-100 <= v <= 100 for v in head), "-100 <= Node.val <= 100"
    assert 0 <= k <= 2 * 10**9, "0 <= k <= 2 * 10^9"
