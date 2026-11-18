"""Maximum Binary Tree II: a maximum binary tree in level order and a value to insert."""

from typing import cast


def check(root: list[int | None], val: int) -> None:
    assert root and root[0] is not None, "the root exists"
    nodes = [v for v in root if v is not None]
    assert 1 <= len(nodes) <= 100, "number of nodes in [1, 100]"
    assert all(1 <= v <= 100 for v in nodes), "1 <= Node.val <= 100"
    assert len(set(nodes)) == len(nodes), "all values of the tree are unique"
    assert 1 <= val <= 100, "1 <= val <= 100"
    assert val not in set(nodes), "b = a + [val] has unique values"
    # level-order decode: parent index of each node, then the max-tree property
    parent = {}
    queue = [0]
    head = 0
    pos = 1
    while head < len(queue) and pos < len(root):
        p = queue[head]
        head += 1
        for _ in range(2):
            if pos < len(root):
                if root[pos] is not None:
                    parent[pos] = p
                    queue.append(pos)
                pos += 1
    for c, p in parent.items():
        assert cast(int, root[p]) > cast(int, root[c]), (
            "every node is greater than all values in its subtree"
        )
