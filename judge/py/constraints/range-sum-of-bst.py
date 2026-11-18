"""Range Sum of BST: a level-order BST with unique values and a [low, high] range."""


def check(root: list, low: int, high: int) -> None:
    assert len(root) >= 1 and root[0] is not None, "tree is non-empty"
    vals = [v for v in root if v is not None]
    assert 1 <= len(vals) <= 2 * 10**4, "number of nodes in [1, 2 * 10^4]"
    assert all(1 <= v <= 10**5 for v in vals), "1 <= Node.val <= 10^5"
    assert len(set(vals)) == len(vals), "all Node.val are unique"
    assert 1 <= low <= high <= 10**5, "1 <= low <= high <= 10^5"
    # level-order structure: children only under existing nodes; build children
    left = {}
    right = {}
    queue = [0]
    pos = 1
    head = 0
    while head < len(queue):
        i = queue[head]
        head += 1
        for side in (left, right):
            if pos < len(root):
                if root[pos] is not None:
                    side[i] = pos
                    queue.append(pos)
                pos += 1
    assert pos >= len(root) or all(v is None for v in root[pos:]), "well-formed level-order tree"
    # BST validity via iterative in-order traversal: strictly increasing
    prev = None
    stack = []
    node = 0
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = left.get(node)
        node = stack.pop()
        assert prev is None or root[node] > prev, "the tree is a valid BST"
        prev = root[node]
        node = right.get(node)
