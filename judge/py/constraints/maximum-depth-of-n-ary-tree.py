"""Maximum Depth of N-ary Tree: an n-ary tree in level-order, child groups separated by null."""


def check(root: list) -> None:
    assert isinstance(root, list), "tree is a level-order list"
    if not root:
        return
    assert root[0] is not None, "root is not null"
    assert len(root) == 1 or root[1] is None, "root is followed by null"
    n = len(root)
    nodes = 1
    depths = [1]
    pos = 2
    i = 0
    max_depth = 1
    while i < len(depths):
        while pos < n and root[pos] is not None:
            nodes += 1
            depths.append(depths[i] + 1)
            max_depth = max(max_depth, depths[i] + 1)
            pos += 1
        pos += 1
        i += 1
    assert pos >= n, "list describes a valid n-ary tree"
    assert nodes == len([v for v in root if v is not None]), "list describes a valid n-ary tree"
    assert nodes <= 10**4, "number of nodes in [0, 10^4]"
    assert max_depth <= 1000, "depth of the tree <= 1000"
