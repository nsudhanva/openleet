"""Second Minimum Node In a Binary Tree: a level-order tree where every node has two or zero
children and equals the smaller of them."""

from typing import cast


def check(root: list[int | None]) -> None:
    assert isinstance(root, list) and root and root[0] is not None, "tree is non-empty"
    kids: dict[int, list[int]] = {}
    queue = [0]
    head = 0
    pos = 1
    while head < len(queue):
        i = queue[head]
        head += 1
        ch = []
        for _ in range(2):
            if pos < len(root):
                if root[pos] is not None:
                    ch.append(pos)
                    queue.append(pos)
                pos += 1
        kids[i] = ch
    assert pos >= len(root), "level-order list has no stray values"
    assert len(queue) == sum(v is not None for v in root), "level-order list is well formed"
    assert 1 <= len(queue) <= 25, "number of nodes in [1, 25]"
    values = cast(list[int], root)
    assert all(isinstance(root[i], int) and 1 <= values[i] <= 2**31 - 1 for i in queue), (
        "1 <= Node.val <= 2^31 - 1"
    )
    assert all(len(c) in (0, 2) for c in kids.values()), (
        "each node has exactly two or zero children"
    )
    assert all(not c or values[i] == min(values[c[0]], values[c[1]]) for i, c in kids.items()), (
        "root.val == min(root.left.val, root.right.val) for each internal node"
    )
