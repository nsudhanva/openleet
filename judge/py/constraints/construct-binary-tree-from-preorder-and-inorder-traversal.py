"""Construct Binary Tree from Preorder and Inorder Traversal: two traversals of one tree."""


def check(preorder: list[int], inorder: list[int]) -> None:
    n = len(preorder)
    assert 1 <= n <= 3000, "1 <= preorder.length <= 3000"
    assert len(inorder) == n, "inorder.length == preorder.length"
    assert all(-3000 <= x <= 3000 for x in preorder + inorder), (
        "-3000 <= preorder[i], inorder[i] <= 3000"
    )
    assert len(set(preorder)) == n and len(set(inorder)) == n, (
        "preorder and inorder consist of unique values"
    )
    assert set(inorder) == set(preorder), "Each value of inorder also appears in preorder"
    pos = {v: i for i, v in enumerate(inorder)}
    stack = [(0, n - 1, 0, n - 1)]  # preorder range, inorder range
    while stack:
        pl, pr, il, ir = stack.pop()
        if pl > pr:
            continue
        k = pos[preorder[pl]]
        assert il <= k <= ir, "preorder and inorder are traversals of the same tree"
        left = k - il
        stack.append((pl + 1, pl + left, il, k - 1))
        stack.append((pl + left + 1, pr, k + 1, ir))
