"""Minimum Flips in Binary Tree to Get Result: a boolean expression tree in level-order form."""


def check(root: list, result: bool) -> None:
    assert root and root[0] is not None, "the root exists"
    vals = {0: root[0]}
    kids: dict[int, list[int]] = {}
    queue = [0]
    pos = 1
    head = 0
    while head < len(queue):
        i = queue[head]
        head += 1
        kids[i] = []
        for _ in range(2):
            if pos < len(root):
                if root[pos] is not None:
                    vals[pos] = root[pos]
                    queue.append(pos)
                    kids[i].append(pos)
                else:
                    kids[i].append(-1)
                pos += 1
            else:
                kids[i].append(-1)
    assert pos >= len(root), "valid level-order list"
    assert 1 <= len(vals) <= 10**5, "number of nodes in [1, 10^5]"
    assert all(isinstance(v, int) and 0 <= v <= 5 for v in vals.values()), "0 <= Node.val <= 5"
    for i, v in vals.items():
        count = sum(k != -1 for k in kids[i])
        if v in (0, 1):
            assert count == 0, "leaf nodes have a value of 0 or 1"
        elif v == 5:
            assert count == 1, "NOT nodes have 1 child"
        else:
            assert count == 2, "OR, AND, and XOR nodes have 2 children"
