"""Equal Tree Partition: a binary tree as a level-order list."""


def check(root: list) -> None:
    assert isinstance(root, list) and root, "root is a non-empty level-order list"
    assert root[0] is not None, "the tree has a root"
    # Level-order: each non-null node consumes two slots for its children.
    nodes = 0
    slots = 1
    for v in root:
        assert slots > 0, "level-order list has no slot for this node"
        slots -= 1
        if v is not None:
            assert isinstance(v, int), "node values are integers"
            assert -(10**5) <= v <= 10**5, "-10^5 <= Node.val <= 10^5"
            nodes += 1
            slots += 2
    assert 1 <= nodes <= 10**4, "the number of nodes is in the range [1, 10^4]"
