"""Parallel Courses III: n courses, a DAG of unique [prev, next] pairs and course times."""


def check(n: int, relations: list[list[int]], time: list[int]) -> None:
    assert isinstance(relations, list) and isinstance(time, list), "relations and time are lists"
    assert 1 <= n <= 5 * 10**4, "1 <= n <= 5 * 10^4"
    assert 0 <= len(relations) <= min(n * (n - 1) // 2, 5 * 10**4), (
        "0 <= relations.length <= min(n * (n - 1) / 2, 5 * 10^4)"
    )
    assert all(len(r) == 2 for r in relations), "relations[j].length == 2"
    assert all(1 <= a <= n and 1 <= b <= n for a, b in relations), (
        "1 <= prevCoursej, nextCoursej <= n"
    )
    assert all(a != b for a, b in relations), "prevCoursej != nextCoursej"
    assert len({(a, b) for a, b in relations}) == len(relations), "all the pairs are unique"
    assert len(time) == n, "time.length == n"
    assert all(1 <= t <= 10**4 for t in time), "1 <= time[i] <= 10^4"
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
