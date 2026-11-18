"""Longest Path With Different Adjacent Characters: a parent array of a tree and node labels."""


def check(parent: list[int], s: str) -> None:
    n = len(parent)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert isinstance(s, str) and len(s) == n, "n == parent.length == s.length"
    assert parent[0] == -1, "parent[0] == -1"
    assert all(0 <= parent[i] <= n - 1 for i in range(1, n)), (
        "0 <= parent[i] <= n - 1 for all i >= 1"
    )
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
    # valid tree: every node reaches the root
    state = [0] * n  # 0 unseen, 1 on path, 2 reaches root
    state[0] = 2
    for i in range(1, n):
        path = []
        v = i
        while state[v] == 0:
            state[v] = 1
            path.append(v)
            v = parent[v]
        assert state[v] == 2, "parent represents a valid tree"
        for u in path:
            state[u] = 2
