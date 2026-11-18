"""Delete Nodes And Return Forest: a level-order tree of distinct values, and values to delete."""


def _attach(t: list) -> tuple[list[int], dict[int, int], dict[int, int]]:
    """Values of the nodes a level-order list really builds, with left/right child positions."""
    if not t or t[0] is None:
        return [], {}, {}
    vals = [t[0]]
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    queue = [0]
    head = 0
    i = 1
    while head < len(queue) and i < len(t):
        p = queue[head]
        head += 1
        for side in (left, right):
            if i < len(t) and t[i] is not None:
                vals.append(t[i])
                side[p] = len(vals) - 1
                queue.append(len(vals) - 1)
            i += 1
    return vals, left, right


def check(root: list[int | None], to_delete: list[int]) -> None:
    assert isinstance(root, list), "root is a level-order list"
    vals, _, _ = _attach(root)
    assert len(vals) <= 1000, "the number of nodes in the given tree is at most 1000"
    assert all(1 <= v <= 1000 for v in vals), "each node has a value between 1 and 1000"
    assert len(set(vals)) == len(vals), "each node has a distinct value"
    assert len(to_delete) <= 1000, "to_delete.length <= 1000"
    assert all(1 <= v <= 1000 for v in to_delete), "to_delete values are between 1 and 1000"
    assert len(set(to_delete)) == len(to_delete), "to_delete contains distinct values"
