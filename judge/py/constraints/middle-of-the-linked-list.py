"""Middle of the Linked List: a linked list as a value list."""


def check(head: list[int]) -> None:
    assert 1 <= len(head) <= 100, "number of nodes in [1, 100]"
    assert all(1 <= v <= 100 for v in head), "1 <= Node.val <= 100"
