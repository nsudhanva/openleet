"""Construct Binary Search Tree from Preorder Traversal: distinct values in preorder."""


def check(preorder: list[int]) -> None:
    assert 1 <= len(preorder) <= 100, "1 <= preorder.length <= 100"
    assert all(1 <= x <= 1000 for x in preorder), "1 <= preorder[i] <= 1000"
    assert len(set(preorder)) == len(preorder), "All the values of preorder are unique"
