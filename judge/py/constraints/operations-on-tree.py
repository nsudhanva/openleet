"""Operations on Tree: a design class LockingTree built from a parent array, then lock,
unlock, upgrade."""


def check(ops: list[str], args: list[list]) -> None:
    assert len(ops) == len(args) and ops, "ops and args have the same non-zero length"
    assert ops[0] == "LockingTree", "first call is the constructor"
    assert all(o in ("lock", "unlock", "upgrade") for o in ops[1:]), (
        "calls are lock, unlock, upgrade"
    )
    assert len(args[0]) == 1, "constructor takes parent"
    parent = args[0][0]
    n = len(parent)
    assert 2 <= n <= 2000, "2 <= n <= 2000"
    assert parent[0] == -1, "parent[0] == -1"
    assert all(0 <= p <= n - 1 for p in parent[1:]), "0 <= parent[i] <= n - 1 for i != 0"
    # valid tree: every node reaches the root without a cycle
    ok = [False] * n
    ok[0] = True
    for start in range(1, n):
        path = []
        v = start
        seen = set()
        while not ok[v]:
            assert v not in seen, "parent represents a valid tree"
            seen.add(v)
            path.append(v)
            v = parent[v]
        for u in path:
            ok[u] = True
    assert len(ops) - 1 <= 2000, "at most 2000 calls in total to lock, unlock, and upgrade"
    for a in args[1:]:
        assert len(a) == 2, "each call takes num and user"
        assert 0 <= a[0] <= n - 1, "0 <= num <= n - 1"
        assert 1 <= a[1] <= 10**4, "1 <= user <= 10^4"
