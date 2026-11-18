"""Verify Preorder Sequence in Binary Search Tree: a list of distinct integers."""


def check(preorder: list[int]) -> None:
    assert 1 <= len(preorder) <= 10**4, "1 <= preorder.length <= 10^4"
    assert all(1 <= v <= 10**4 for v in preorder), "1 <= preorder[i] <= 10^4"
    assert len(set(preorder)) == len(preorder), "all the elements of preorder are unique"
