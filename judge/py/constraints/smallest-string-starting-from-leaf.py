"""Smallest String Starting From Leaf: a level-order binary tree of values 0..25."""


def check(root: list) -> None:
    assert root and root[0] is not None, "the tree has a root"
    count = sum(v is not None for v in root)
    assert 1 <= count <= 8500, "number of nodes is in the range [1, 8500]"
    assert all(isinstance(v, int) and 0 <= v <= 25 for v in root if v is not None), (
        "0 <= Node.val <= 25"
    )
