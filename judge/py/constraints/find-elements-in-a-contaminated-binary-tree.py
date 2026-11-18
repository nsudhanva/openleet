"""Find Elements in a Contaminated Binary Tree: FindElements(root) then find(target) calls."""

from collections import deque


def _tree(root: list) -> tuple[list[int], int]:
    """Return (non-null values, height) of a level-order tree list."""
    assert isinstance(root, list) and root and root[0] is not None, (
        "root is a non-empty level-order tree"
    )
    vals = [root[0]]
    height = 1
    queue = deque([1])
    i = 1
    while queue:
        d = queue.popleft()
        for _ in range(2):
            if i < len(root):
                v = root[i]
                i += 1
                if v is not None:
                    vals.append(v)
                    height = max(height, d + 1)
                    queue.append(d + 1)
    return vals, height


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "FindElements" and len(args[0]) == 1, "the constructor is FindElements(root)"
    vals, height = _tree(args[0][0])
    assert all(v == -1 for v in vals), "TreeNode.val == -1"
    assert height <= 20, "the height of the binary tree is less than or equal to 20"
    assert 1 <= len(vals) <= 10**4, "the total number of nodes is between [1, 10^4]"
    calls = ops[1:]
    assert all(o == "find" for o in calls), "the only other operation is find"
    assert 1 <= len(calls) <= 10**4, "total calls of find() is between [1, 10^4]"
    assert all(len(a) == 1 and 0 <= a[0] <= 10**6 for a in args[1:]), "0 <= target <= 10^6"
