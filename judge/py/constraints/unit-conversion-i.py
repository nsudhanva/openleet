"""Unit Conversion I: n-1 directed conversion edges forming a tree out of unit 0."""


def check(conversions: list[list[int]]) -> None:
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
    parent = {}
    children = [[] for _ in range(n)]
    for a, b, _ in conversions:
        assert b not in parent and b != 0, "unit 0 reaches every unit by a unique forward path"
        parent[b] = a
        children[a].append(b)
    seen = [False] * n
    seen[0] = True
    stack = [0]
    while stack:
        u = stack.pop()
        for v in children[u]:
            if not seen[v]:
                seen[v] = True
                stack.append(v)
    assert all(seen), "unit 0 can be converted into any other unit"
