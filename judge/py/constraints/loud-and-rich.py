"""Loud and Rich: richer pairs [a, b] (a richer than b) and a quietness list."""


def check(richer: list[list[int]], quiet: list[int]) -> None:
    n = len(quiet)
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(0 <= q < n for q in quiet), "0 <= quiet[i] < n"
    assert len(set(quiet)) == n, "all the values of quiet are unique"
    assert 0 <= len(richer) <= n * (n - 1) // 2, "0 <= richer.length <= n * (n - 1) / 2"
    assert all(len(r) == 2 for r in richer), "richer[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in richer), "0 <= ai, bi < n"
    assert all(a != b for a, b in richer), "ai != bi"
    assert len({(a, b) for a, b in richer}) == len(richer), "all the pairs of richer are unique"
    # Logical consistency: the "richer than" graph has no cycle (Kahn's algorithm).
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in richer:
        adj[a].append(b)
        indeg[b] += 1
    stack = [i for i in range(n) if indeg[i] == 0]
    seen = 0
    while stack:
        u = stack.pop()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                stack.append(v)
    assert seen == n, "the observations in richer are all logically consistent"
