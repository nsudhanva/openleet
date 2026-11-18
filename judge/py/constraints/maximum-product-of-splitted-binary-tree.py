"""Maximum Product of Splitted Binary Tree: a binary tree as a level-order list."""


def check(root: list) -> None:
    assert len(root) >= 1 and root[0] is not None, "the tree is non-empty"
    pos, level, count = 1, 1, 1
    while pos < len(root) and level:
        chunk = root[pos : pos + 2 * level]
        pos += len(chunk)
        level = sum(v is not None for v in chunk)
        count += level
    assert pos == len(root), "root is a valid level-order tree"
    assert 2 <= count <= 5 * 10**4, "the number of nodes is in the range [2, 5 * 10^4]"
    assert all(1 <= v <= 10**4 for v in root if v is not None), "1 <= Node.val <= 10^4"
