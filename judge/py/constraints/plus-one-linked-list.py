"""Plus One Linked List: digits of a non-negative integer as a list of node values."""


def check(head: list[int]) -> None:
    assert 1 <= len(head) <= 100, "number of nodes is in [1, 100]"
    assert all(0 <= v <= 9 for v in head), "0 <= Node.val <= 9"
    assert head[0] != 0 or len(head) == 1, "no leading zeros except for the zero itself"
