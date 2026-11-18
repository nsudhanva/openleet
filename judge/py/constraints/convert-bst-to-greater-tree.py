"""Convert BST to Greater Tree: a level-order binary search tree with unique values."""


def check(root: list) -> None:
    assert isinstance(root, list), "root is a level-order list"
    n = len(root)
    present = [v for v in root if v is not None]
    assert all(isinstance(v, int) for v in present), "Node.val is an integer"
    assert len(present) <= 10**4, "The number of nodes in the tree is in the range [0, 10^4]"
    assert all(-(10**4) <= v <= 10**4 for v in present), "-10^4 <= Node.val <= 10^4"
    assert len(set(present)) == len(present), "All the values in the tree are unique"
    if n:
        assert root[0] is not None, "the root is present"
    # Children of each present node, in level order, are the next two slots.
    left: dict[int, int] = {}
    right: dict[int, int] = {}
    queue = [0] if n else []
    nxt = 1
    for idx in queue:
        for side in (left, right):
            if nxt < n:
                if root[nxt] is not None:
                    side[idx] = nxt
                    queue.append(nxt)
                nxt += 1
    # An in-order walk of a valid binary search tree is strictly increasing.
    prev = None
    stack: list[int] = []
    cur = 0 if n else None
    while stack or cur is not None:
        while cur is not None:
            stack.append(cur)
            cur = left.get(cur)
        cur = stack.pop()
        assert prev is None or root[cur] > prev, "root is a valid binary search tree"
        prev = root[cur]
        cur = right.get(cur)
