"""Unit Conversion II: n-1 conversion edges forming a tree on units 0..n-1, plus unit queries."""


def check(conversions: list[list[int]], queries: list[list[int]]) -> None:
    m = len(conversions)
    n = m + 1
    assert 2 <= n <= 10**5, "2 <= n <= 10^5"
    assert all(isinstance(c, list) and len(c) == 3 for c in conversions), (
        "conversions[i].length == 3"
    )
    assert all(0 <= a < n and 0 <= b < n for a, b, _ in conversions), (
        "0 <= sourceUniti, targetUniti < n"
    )
    assert all(1 <= f <= 10**9 for _, _, f in conversions), "1 <= conversionFactori <= 10^9"
    assert 1 <= len(queries) <= 10**5, "1 <= q <= 10^5"
    assert all(isinstance(q, list) and len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in queries), "0 <= unitAi, unitBi < n"
    adj = [[] for _ in range(n)]
    for a, b, _ in conversions:
        adj[a].append(b)
        adj[b].append(a)
    seen = [False] * n
    seen[0] = True
    stack = [0]
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    assert all(seen), "unit 0 can be converted into any other unit"
