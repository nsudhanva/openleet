"""Construct Binary Tree from Inorder and Postorder Traversal: two traversals of one tree."""


def check(inorder: list[int], postorder: list[int]) -> None:
    n = len(inorder)
    assert 1 <= n <= 3000, "1 <= inorder.length <= 3000"
    assert len(postorder) == n, "postorder.length == inorder.length"
    assert all(-3000 <= x <= 3000 for x in inorder + postorder), (
        "-3000 <= inorder[i], postorder[i] <= 3000"
    )
    assert len(set(inorder)) == n and len(set(postorder)) == n, (
        "inorder and postorder consist of unique values"
    )
    assert set(inorder) == set(postorder), "Each value of postorder also appears in inorder"
    pos = {v: i for i, v in enumerate(inorder)}
    stack = [(0, n - 1, 0, n - 1)]  # inorder range, postorder range
    while stack:
        il, ir, pl, pr = stack.pop()
        if il > ir:
            continue
        k = pos[postorder[pr]]
        assert il <= k <= ir, "inorder and postorder are traversals of the same tree"
        left = k - il
        stack.append((il, k - 1, pl, pl + left - 1))
        stack.append((k + 1, ir, pl + left, pr - 1))
