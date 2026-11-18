"""Complete Binary Tree Inserter: a complete tree, then insert and get_root calls."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) >= 1, "one argument list per operation"
    assert ops[0] == "CBTInserter" and len(args[0]) == 1, "constructor takes root"
    root = args[0][0]
    assert isinstance(root, list) and root and root[0] is not None, "root is not empty"
    seen_none = False
    for v in root:
        if v is None:
            seen_none = True
        else:
            assert not seen_none, "root is a complete binary tree"
            assert isinstance(v, int), "Node.val is an integer"
            assert 0 <= v <= 5000, "0 <= Node.val <= 5000"
    assert len(root) - sum(v is None for v in root) <= 1000, (
        "The number of nodes in the tree will be in the range [1, 1000]"
    )
    assert len(ops) - 1 <= 10**4, "At most 10^4 calls will be made to insert and get_root"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op in ("insert", "get_root"), "only insert and get_root are called"
        assert isinstance(a, list), "arguments are a list"
        if op == "insert":
            assert len(a) == 1 and isinstance(a[0], int), "insert takes val"
            assert 0 <= a[0] <= 5000, "0 <= val <= 5000"
        else:
            assert len(a) == 0, "get_root takes no arguments"
