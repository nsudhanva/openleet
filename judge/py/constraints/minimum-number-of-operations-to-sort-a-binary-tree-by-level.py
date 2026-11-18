"""Minimum Number of Operations to Sort a Binary Tree by Level: a level-order binary tree with
unique values."""


def check(root: list) -> None:
    assert isinstance(root, list) and len(root) >= 1, "the tree has at least one node"
    assert root[0] is not None, "the root is not null"
    # level-order: each non-null node consumes the next two entries as its children
    parents = [0]
    p = 0
    i = 1
    while i < len(root):
        assert p < len(parents), "a valid level-order binary tree"
        for _ in range(2):
            if i < len(root):
                if root[i] is not None:
                    parents.append(i)
                i += 1
        p += 1
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 10**5, "the number of nodes is in the range [1, 10^5]"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for v in vals), "1 <= Node.val <= 10^5"
    assert len(set(vals)) == len(vals), "all the values of the tree are unique"
