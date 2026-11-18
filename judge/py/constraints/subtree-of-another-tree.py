"""Subtree of Another Tree: two binary trees in level-order lists."""


def _check_tree(tree: list, name: str, lo: int, hi: int) -> None:
    assert isinstance(tree, list) and len(tree) >= 1, f"{name} is a non-empty level-order list"
    assert tree[0] is not None, f"{name} has a root"
    vals = [v for v in tree if v is not None]
    assert lo <= len(vals) <= hi, f"number of nodes in {name} is in [{lo}, {hi}]"
    assert all(-(10**4) <= v <= 10**4 for v in vals), f"-10^4 <= {name}.val <= 10^4"


def check(root: list, subRoot: list) -> None:
    _check_tree(root, "root", 1, 2000)
    _check_tree(subRoot, "subRoot", 1, 1000)
