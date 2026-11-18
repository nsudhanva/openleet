"""Delete N Nodes After M Nodes of a Linked List: a linked list (list of values) and m, n."""


def check(head: list[int], m: int, n: int) -> None:
    assert 1 <= len(head) <= 10**4, "the number of nodes is in the range [1, 10^4]"
    assert all(1 <= v <= 10**6 for v in head), "1 <= Node.val <= 10^6"
    assert 1 <= m <= 1000, "1 <= m <= 1000"
    assert 1 <= n <= 1000, "1 <= n <= 1000"
