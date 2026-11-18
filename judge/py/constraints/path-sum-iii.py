"""Path Sum III: a binary tree in level order and a target sum."""


def check(root: list, targetSum: int) -> None:
    assert isinstance(root, list), "root is a level-order list"
    nodes = [v for v in root if v is not None]
    assert 0 <= len(nodes) <= 1000, "The number of nodes in the tree is in the range [0, 1000]"
    assert all(isinstance(v, int) and -(10**9) <= v <= 10**9 for v in nodes), (
        "-10^9 <= Node.val <= 10^9"
    )
    assert not root or root[0] is not None, "the root is not null"
    assert isinstance(targetSum, int) and -1000 <= targetSum <= 1000, "-1000 <= targetSum <= 1000"
