"""Leaf-Similar Trees: two binary trees as level-order lists."""


def _tree(name: str, t: list) -> None:
    assert len(t) >= 1 and t[0] is not None, f"{name} has a root"
    pending = 1  # child slots opened by nodes seen so far
    i = 1
    nodes = 1
    while i < len(t) and pending:
        take = min(2 * pending, len(t) - i)
        chunk = t[i : i + take]
        i += take
        pending = sum(v is not None for v in chunk)
        nodes += pending
    assert i == len(t) and all(v is None for v in t[i:]), f"{name} is a valid level-order tree"
    assert 1 <= nodes <= 200, f"the number of nodes in {name} is in [1, 200]"
    assert all(v is None or (isinstance(v, int) and 0 <= v <= 200) for v in t), (
        f"{name} values are in [0, 200]"
    )


def check(root1: list, root2: list) -> None:
    _tree("root1", root1)
    _tree("root2", root2)
