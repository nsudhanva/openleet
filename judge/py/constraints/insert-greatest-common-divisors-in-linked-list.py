"""Insert Greatest Common Divisors in Linked List: a list of node values."""


def check(head: list[int]) -> None:
    assert 1 <= len(head) <= 5000, "number of nodes is in the range [1, 5000]"
    assert all(1 <= v <= 1000 for v in head), "1 <= Node.val <= 1000"
