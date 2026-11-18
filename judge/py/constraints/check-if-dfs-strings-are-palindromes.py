"""Check if DFS Strings Are Palindromes: a parent array of a tree rooted at 0 and node letters."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(parent: list[int], s: str) -> None:
    n = len(parent)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(s) == n, "n == parent.length == s.length"
    assert parent[0] == -1, "parent[0] == -1"
    assert all(0 <= p <= n - 1 for p in parent[1:]), "0 <= parent[i] <= n - 1 for all i >= 1"
    assert set(s) <= LOWER, "s consists only of lowercase English letters"
    children: list[list[int]] = [[] for _ in range(n)]
    for i in range(1, n):
        children[parent[i]].append(i)
    seen = 1
    stack = [0]
    while stack:
        for c in children[stack.pop()]:
            seen += 1
            stack.append(c)
    assert seen == n, "parent represents a valid tree"
