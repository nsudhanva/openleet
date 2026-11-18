"""All Nodes Distance K in Binary Tree: a level-order tree, a target node value and k."""


def _tree_values(tree: list, name: str) -> list[int]:
    assert isinstance(tree, list), f"{name} is a level-order list"
    tree = list(tree)
    while tree and tree[-1] is None:
        tree.pop()
    if not tree:
        return []
    assert tree[0] is not None, f"{name} root is not missing"
    values = [v for v in tree if v is not None]
    # each present node consumes two child slots; the list has no slots beyond those
    assert len(tree) <= 1 + 2 * len(values), f"{name} is a valid level-order tree"
    return values


def check(root: list[int | None], target: int, k: int) -> None:
    values = _tree_values(root, "root")
    assert 1 <= len(values) <= 500, "The number of nodes in the tree is in the range [1, 500]"
    assert all(isinstance(v, int) and 0 <= v <= 500 for v in values), "0 <= Node.val <= 500"
    assert len(set(values)) == len(values), "All the values Node.val are unique"
    assert target in values, "target is the value of one of the nodes in the tree"
    assert 0 <= k <= 1000, "0 <= k <= 1000"
