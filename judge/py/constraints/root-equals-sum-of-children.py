"""Root Equals Sum of Children: a level-order tree of exactly three nodes."""


def check(root: list) -> None:
    assert isinstance(root, list) and len(root) == 3, (
        "the tree consists only of the root, its left child, and its right child"
    )
    assert all(v is not None for v in root), "the tree has a root, a left child and a right child"
    assert all(-100 <= v <= 100 for v in root), "-100 <= Node.val <= 100"
