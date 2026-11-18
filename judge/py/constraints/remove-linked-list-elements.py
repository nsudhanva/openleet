"""Remove Linked List Elements: a linked list of small positive values and a value to remove."""


def check(head: list[int], val: int) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert 0 <= len(head) <= 10**4, "number of nodes in [0, 10^4]"
    assert all(1 <= v <= 50 for v in head), "1 <= Node.val <= 50"
    assert isinstance(val, int), "val is an integer"
    assert 0 <= val <= 50, "0 <= val <= 50"
