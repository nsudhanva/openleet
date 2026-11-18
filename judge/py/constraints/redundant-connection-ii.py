"""Redundant Connection II: n directed edges forming a rooted tree plus an edge."""


def _is_rooted_tree(n: int, edges: list[list[int]], skip: int) -> bool:
    parent = [0] * (n + 1)
    children: list[list[int]] = [[] for _ in range(n + 1)]
    for i, (u, v) in enumerate(edges):
        if i == skip:
            continue
        if parent[v]:
            return False
        parent[v] = u
        children[u].append(v)
    roots = [v for v in range(1, n + 1) if not parent[v]]
    if len(roots) != 1:
        return False
    seen, stack = {roots[0]}, [roots[0]]
    while stack:
        for c in children[stack.pop()]:
            if c not in seen:
                seen.add(c)
                stack.append(c)
    return len(seen) == n


def check(edges: list[list[int]]) -> None:
    n = len(edges)
    assert 3 <= n <= 1000, "3 <= n <= 1000"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(1 <= u <= n and 1 <= v <= n for u, v in edges), "1 <= ui, vi <= n"
    assert all(u != v for u, v in edges), "ui != vi"
    assert len({tuple(e) for e in edges}) == n, (
        "the added edge was not an edge that already existed"
    )
    indeg: dict[int, list[int]] = {}
    for i, (_, v) in enumerate(edges):
        indeg.setdefault(v, []).append(i)
    twice = [ix for ix in indeg.values() if len(ix) == 2]
    assert all(len(ix) <= 2 for ix in indeg.values()), (
        "a rooted tree plus one edge: at most two parents"
    )
    candidates = twice[0] if twice else range(n)
    assert any(_is_rooted_tree(n, edges, i) for i in candidates), (
        "a rooted tree with one additional directed edge"
    )
