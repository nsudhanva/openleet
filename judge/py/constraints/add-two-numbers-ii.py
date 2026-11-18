"""Add Two Numbers II: two digit lists, most significant digit first."""


def check(l1: list[int], l2: list[int]) -> None:
    for lst in (l1, l2):
        assert 1 <= len(lst) <= 100, "number of nodes in each list is in [1, 100]"
        assert all(0 <= d <= 9 for d in lst), "0 <= Node.val <= 9"
        assert len(lst) == 1 or lst[0] != 0, "the number has no leading zeros"
