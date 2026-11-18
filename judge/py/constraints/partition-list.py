"""Partition List: a linked list of values and a pivot x."""


def check(head: list[int], x: int) -> None:
    assert isinstance(head, list), "head is a list"
    assert 0 <= len(head) <= 200, "The number of nodes in the list is in the range [0, 200]"
    assert all(isinstance(v, int) and -100 <= v <= 100 for v in head), "-100 <= Node.val <= 100"
    assert isinstance(x, int) and -200 <= x <= 200, "-200 <= x <= 200"
