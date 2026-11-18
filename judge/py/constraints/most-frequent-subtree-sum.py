"""Most Frequent Subtree Sum: a binary tree as a level-order list with None for missing children."""


def check(root: list) -> None:
    assert root and root[0] is not None, "the tree has at least one node"
    nodes = 1
    i = 1
    queue = 1  # nodes waiting to take children
    while i < len(root) and queue:
        queue -= 1
        for _ in range(2):
            if i < len(root):
                if root[i] is not None:
                    queue += 1
                    nodes += 1
                i += 1
    assert i >= len(root), "valid level-order encoding of a binary tree"
    assert 1 <= nodes <= 10**4, "the number of nodes is in the range [1, 10^4]"
    assert all(-(10**5) <= v <= 10**5 for v in root if v is not None), "-10^5 <= Node.val <= 10^5"
