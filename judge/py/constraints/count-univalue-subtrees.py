"""Count Univalue Subtrees: a binary tree as a level-order list."""


def check(root: list) -> None:
    assert isinstance(root, list), "root is a level-order list"
    if root:
        assert root[0] is not None, "the root of a non-empty tree is not null"
    slots = 1 if root else 0  # child positions the nodes so far can fill
    nodes = 0
    for i, v in enumerate(root):
        assert i < slots, "level-order list lists children only under existing nodes"
        if v is not None:
            assert isinstance(v, int), "Node.val is an integer"
            assert -1000 <= v <= 1000, "-1000 <= Node.val <= 1000"
            nodes += 1
            slots += 2
    assert 0 <= nodes <= 1000, "number of nodes in the range [0, 1000]"
