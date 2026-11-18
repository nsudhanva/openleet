"""Remove Nth Node From End of List: a short linked list and n."""


def check(head: list[int], n: int) -> None:
    assert isinstance(head, list), "head is a list of values"
    assert isinstance(n, int), "n is an integer"
    assert 1 <= len(head) <= 30, "1 <= sz <= 30"
    assert all(0 <= v <= 100 for v in head), "0 <= Node.val <= 100"
    assert 1 <= n <= len(head), "1 <= n <= sz"
