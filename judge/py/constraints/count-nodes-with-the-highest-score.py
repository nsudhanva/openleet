"""Count Nodes With the Highest Score: parent array of a binary tree rooted at 0."""


def check(parents: list[int]) -> None:
    n = len(parents)
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert parents[0] == -1, "parents[0] == -1"
    assert all(0 <= p <= n - 1 for p in parents[1:]), "0 <= parents[i] <= n - 1 for i != 0"
    children: list[list[int]] = [[] for _ in range(n)]
    for i in range(1, n):
        children[parents[i]].append(i)
    assert all(len(c) <= 2 for c in children), "parents represents a binary tree"
    seen = 1
    stack = [0]
    while stack:
        for c in children[stack.pop()]:
            seen += 1
            stack.append(c)
    assert seen == n, "parents represents a valid tree rooted at 0"
