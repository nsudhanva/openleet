"""Course Schedule IV: numCourses, an acyclic list of unique prerequisite pairs, and queries."""


def check(numCourses: int, prerequisites: list[list[int]], queries: list[list[int]]) -> None:
    assert 2 <= numCourses <= 100, "2 <= numCourses <= 100"
    assert 0 <= len(prerequisites) <= numCourses * (numCourses - 1) // 2, (
        "0 <= prerequisites.length <= numCourses * (numCourses - 1) / 2"
    )
    assert all(len(p) == 2 for p in prerequisites), "prerequisites[i].length == 2"
    assert all(0 <= v <= numCourses - 1 for p in prerequisites for v in p), (
        "0 <= ai, bi <= numCourses - 1"
    )
    assert all(a != b for a, b in prerequisites), "ai != bi"
    assert len({tuple(p) for p in prerequisites}) == len(prerequisites), (
        "all the pairs [ai, bi] are unique"
    )
    indeg = [0] * numCourses
    adj: list[list[int]] = [[] for _ in range(numCourses)]
    for a, b in prerequisites:
        adj[a].append(b)
        indeg[b] += 1
    stack = [v for v in range(numCourses) if indeg[v] == 0]
    seen = 0
    while stack:
        v = stack.pop()
        seen += 1
        for w in adj[v]:
            indeg[w] -= 1
            if indeg[w] == 0:
                stack.append(w)
    assert seen == numCourses, "the prerequisites graph has no cycles"
    assert 1 <= len(queries) <= 10**4, "1 <= queries.length <= 10^4"
    assert all(len(q) == 2 for q in queries), "queries[i].length == 2"
    assert all(0 <= v <= numCourses - 1 for q in queries for v in q), (
        "0 <= ui, vi <= numCourses - 1"
    )
    assert all(u != v for u, v in queries), "ui != vi"
