"""Maximum Profit from Trading Stocks with Discounts: employees, prices, a boss tree, a budget."""


def check(
    n: int, present: list[int], future: list[int], hierarchy: list[list[int]], budget: int
) -> None:
    assert 1 <= n <= 160, "1 <= n <= 160"
    assert len(present) == n and len(future) == n, "present.length, future.length == n"
    assert all(1 <= v <= 50 for v in present), "1 <= present[i] <= 50"
    assert all(1 <= v <= 50 for v in future), "1 <= future[i] <= 50"
    assert len(hierarchy) == n - 1, "hierarchy.length == n - 1"
    assert all(len(e) == 2 for e in hierarchy), "hierarchy[i] == [ui, vi]"
    assert all(1 <= u <= n and 1 <= v <= n for u, v in hierarchy), "1 <= ui, vi <= n"
    assert all(u != v for u, v in hierarchy), "ui != vi"
    assert 1 <= budget <= 160, "1 <= budget <= 160"
    assert len({(u, v) for u, v in hierarchy}) == len(hierarchy), "There are no duplicate edges"
    children: dict[int, list[int]] = {}
    for u, v in hierarchy:
        children.setdefault(u, []).append(v)
    seen = {1}
    stack = [1]
    while stack:
        for c in children.get(stack.pop(), []):
            assert c not in seen, "The input graph hierarchy has no cycles"
            seen.add(c)
            stack.append(c)
    assert len(seen) == n, "Employee 1 is the direct or indirect boss of every employee"
