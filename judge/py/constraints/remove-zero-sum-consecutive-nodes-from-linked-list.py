"""Remove Zero Sum Consecutive Nodes from Linked List: a linked list of small integers."""


def check(head: list[int]) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert 1 <= len(head) <= 1000, "between 1 and 1000 nodes"
    assert all(-1000 <= v <= 1000 for v in head), "-1000 <= node.val <= 1000"
