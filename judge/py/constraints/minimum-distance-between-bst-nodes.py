"""Minimum Distance Between BST Nodes: a binary search tree in level-order form."""


def check(root: list) -> None:
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
    assert 2 <= len(vals) <= 100, "number of nodes in [2, 100]"
    assert all(isinstance(v, int) and 0 <= v <= 10**5 for v in vals.values()), (
        "0 <= Node.val <= 10^5"
    )
    stack = [(0, 0, 10**5)]
    while stack:
        i, lo, hi = stack.pop()
        v = vals[i]
        assert lo <= v <= hi, "the tree is a binary search tree"
        left, right = kids[i]
        if left != -1:
            stack.append((left, lo, v))
        if right != -1:
            stack.append((right, v, hi))
