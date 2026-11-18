"""Amount of Time for Binary Tree to Be Infected: a level-order tree and a start value."""


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


def check(root: list[int | None], start: int) -> None:
    values = _tree_values(root, "root")
    assert 1 <= len(values) <= 10**5, "The number of nodes in the tree is in the range [1, 10^5]"
    assert all(isinstance(v, int) and 1 <= v <= 10**5 for v in values), "1 <= Node.val <= 10^5"
    assert len(set(values)) == len(values), "Each node has a unique value"
    assert start in set(values), "A node with a value of start exists in the tree"
