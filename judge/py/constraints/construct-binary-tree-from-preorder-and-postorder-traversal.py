"""Construct Binary Tree from Preorder and Postorder Traversal: two traversals of one tree."""


def check(preorder: list[int], postorder: list[int]) -> None:
    n = len(preorder)
    assert 1 <= n <= 30, "1 <= preorder.length <= 30"
    assert all(1 <= x <= n for x in preorder), "1 <= preorder[i] <= preorder.length"
    assert len(set(preorder)) == n, "All the values of preorder are unique"
    assert len(postorder) == n, "postorder.length == preorder.length"
    assert all(1 <= x <= n for x in postorder), "1 <= postorder[i] <= postorder.length"
    assert len(set(postorder)) == n, "All the values of postorder are unique"
    pos = {v: i for i, v in enumerate(postorder)}
    stack = [(0, n - 1, 0, n - 1)]  # preorder range, postorder range
    while stack:
        pl, pr, ql, qr = stack.pop()
        if pl > pr:
            continue
        assert preorder[pl] == postorder[qr], (
            "preorder and postorder are traversals of the same binary tree"
        )
        if pl == pr:
            continue
        idx = pos[preorder[pl + 1]]
        assert ql <= idx < qr, "preorder and postorder are traversals of the same binary tree"
        left = idx - ql + 1
        stack.append((pl + 1, pl + left, ql, idx))
        stack.append((pl + left + 1, pr, idx + 1, qr - 1))
