"""Even Odd Tree: a binary tree in level-order list form."""


def check(root: list[int | None]) -> None:
    assert isinstance(root, list) and root, "the tree is non-empty"
    assert root[0] is not None, "the root is a node"
    nodes = [v for v in root if v is not None]
    assert 1 <= len(nodes) <= 10**5, "the number of nodes in the tree is in the range [1, 10^5]"
    assert all(isinstance(v, int) and 1 <= v <= 10**6 for v in nodes), "1 <= Node.val <= 10^6"
    # every entry after the root needs a parent: the k-th node holds entries 2k+1 and 2k+2
    count = 0
    for j, v in enumerate(root):
        if j > 0:
            assert (j - 1) // 2 < count, "level-order list is a valid tree"
        if v is not None:
            count += 1
