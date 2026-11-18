"""Count Paths That Can Form a Palindrome in a Tree: a parent array and node letters."""


def check(parent: list[int], s: str) -> None:
    n = len(parent)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(s) == n, "n == parent.length == s.length"
    assert parent[0] == -1, "parent[0] == -1"
    assert all(0 <= parent[i] <= n - 1 for i in range(1, n)), (
        "0 <= parent[i] <= n - 1 for all i >= 1"
    )
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
    # valid tree: every node reaches the root 0
    state = [0] * n  # 0 unseen, 1 on path, 2 reaches root
    state[0] = 2
    for i in range(1, n):
        path = []
        j = i
        while state[j] == 0:
            state[j] = 1
            path.append(j)
            j = parent[j]
        assert state[j] == 2, "parent represents a valid tree"
        for j in path:
            state[j] = 2
