"""Parallel Courses II: n courses, a DAG of unique [prev, next] pairs and a per-semester limit k."""


def check(n: int, relations: list[list[int]], k: int) -> None:
    assert isinstance(relations, list), "relations is a list"
    assert 1 <= n <= 15, "1 <= n <= 15"
    assert 1 <= k <= n, "1 <= k <= n"
    assert 0 <= len(relations) <= n * (n - 1) // 2, "0 <= relations.length <= n * (n-1) / 2"
    assert all(len(r) == 2 for r in relations), "relations[i].length == 2"
    assert all(1 <= a <= n and 1 <= b <= n for a, b in relations), (
        "1 <= prevCoursei, nextCoursei <= n"
    )
    assert all(a != b for a, b in relations), "prevCoursei != nextCoursei"
    assert len({(a, b) for a, b in relations}) == len(relations), "all the pairs are unique"
    indeg = [0] * (n + 1)
    adj = [[] for _ in range(n + 1)]
    for a, b in relations:
        adj[a].append(b)
        indeg[b] += 1
    stack = [v for v in range(1, n + 1) if indeg[v] == 0]
    seen = 0
    while stack:
        v = stack.pop()
        seen += 1
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    assert seen == n, "the given graph is a directed acyclic graph"
