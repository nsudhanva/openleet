"""Path Sum II: a binary tree in level order and a target sum."""


def check(root: list, targetSum: int) -> None:
    assert isinstance(root, list), "root is a level-order list"
    nodes = [v for v in root if v is not None]
    assert 0 <= len(nodes) <= 5000, "The number of nodes in the tree is in the range [0, 5000]"
    assert all(isinstance(v, int) and -1000 <= v <= 1000 for v in nodes), (
        "-1000 <= Node.val <= 1000"
    )
    assert not root or root[0] is not None, "the root is not null"
    assert isinstance(targetSum, int) and -1000 <= targetSum <= 1000, "-1000 <= targetSum <= 1000"
