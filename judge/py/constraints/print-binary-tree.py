"""Print Binary Tree: a binary tree in level-order form with between 1 and 10 levels."""


def check(root: list) -> None:
    assert isinstance(root, list) and root, "the tree has at least one node"
    assert root[0] is not None, "the root is not null"
    nodes = 0
    levels = 0
    i = 0
    width = 1
    while i < len(root):
        level = root[i : i + width]
        i += width
        levels += 1
        present = 0
        for v in level:
            if v is not None:
                assert isinstance(v, int), "Node.val is an integer"
                assert -99 <= v <= 99, "-99 <= Node.val <= 99"
                present += 1
        nodes += present
        if present == 0:
            break
        width = present * 2
    assert 1 <= nodes <= 2**10, "the number of nodes is in the range [1, 2^10]"
    assert 1 <= levels <= 10, "the depth of the tree is in the range [1, 10]"
