"""Double a Number Represented as a Linked List: digits of a number, most significant first."""


def check(head: list[int]) -> None:
    assert isinstance(head, list), "list"
    assert 1 <= len(head) <= 10**4, "the number of nodes is in the range [1, 10^4]"
    assert all(isinstance(v, int) and 0 <= v <= 9 for v in head), "0 <= Node.val <= 9"
    assert head[0] != 0 or len(head) == 1, "no leading zeros except the number 0 itself"
