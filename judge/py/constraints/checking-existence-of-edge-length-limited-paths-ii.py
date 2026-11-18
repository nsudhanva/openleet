"""Checking Existence of Edge Length Limited Paths II: design class, n and edges, queries."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and len(ops) >= 1, "ops and args have equal length"
    assert ops[0] == "DistanceLimitedPathsExist", "first op is the constructor"
    assert all(o == "query" for o in ops[1:]), "all later ops are query"
    assert len(args[0]) == 2, "constructor takes n and edgeList"
    n, edges = args[0]
    assert 2 <= n <= 10**4, "2 <= n <= 10^4"
    assert 0 <= len(edges) <= 10**4, "0 <= edgeList.length <= 10^4"
    assert all(len(e) == 3 for e in edges), "edgeList[i].length == 3"
    assert all(0 <= e[0] <= n - 1 and 0 <= e[1] <= n - 1 for e in edges), "0 <= ui, vi <= n-1"
    assert all(e[0] != e[1] for e in edges), "ui != vi"
    assert all(1 <= e[2] <= 10**9 for e in edges), "1 <= disi <= 10^9"
    assert len(ops) - 1 <= 10**4, "At most 10^4 calls will be made to query"
    for a in args[1:]:
        assert len(a) == 3, "query takes p, q, limit"
        p, q, limit = a
        assert 0 <= p <= n - 1 and 0 <= q <= n - 1, "0 <= p, q <= n-1"
        assert p != q, "p != q"
        assert 1 <= limit <= 10**9, "1 <= limit <= 10^9"
