"""Maximum Difference Between Node and Ancestor: a binary tree in level-order."""


def check(root: list) -> None:
    values = tree_values(root)
    assert 2 <= len(values) <= 5000, "number of nodes in [2, 5000]"
    assert all(0 <= v <= 10**5 for v in values), "0 <= Node.val <= 10^5"


def tree_values(tree: list) -> list:
    """Check the root and return the values of the nodes attached to the tree."""
    assert isinstance(tree, list), "tree is a level-order list"
    if not tree:
        return []
    assert tree[0] is not None, "root is not null"
    queue = 1
    pos = 1
    seen = 0
    while seen < queue:
        for _ in range(2):
            if pos < len(tree):
                if tree[pos] is not None:
                    queue += 1
                pos += 1
        seen += 1
    return [v for v in tree[:pos] if v is not None]
