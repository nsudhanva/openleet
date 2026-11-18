"""Kth Ancestor of a Tree Node: a design problem with a parent array and getKthAncestor queries."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "one argument list per operation"
    assert ops[0] == "TreeAncestor" and len(args[0]) == 2, "constructor TreeAncestor(n, parent)"
    n, parent = args[0]
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert len(parent) == n, "parent.length == n"
    assert parent[0] == -1, "parent[0] == -1"
    assert all(0 <= parent[i] < n for i in range(1, n)), "0 <= parent[i] < n for all 0 < i < n"
    assert len(ops) - 1 <= 5 * 10**4, "at most 5 * 10^4 queries"
    for op, a in zip(ops[1:], args[1:], strict=True):
        assert op == "getKthAncestor" and len(a) == 2, "calls are getKthAncestor(node, k)"
        node, k = a
        assert 0 <= node < n, "0 <= node < n"
        assert 1 <= k <= n, "1 <= k <= n"
