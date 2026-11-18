"""Maximum Score of a Node Sequence: node scores and a simple undirected edge list."""


def check(scores: list[int], edges: list[list[int]]) -> None:
    n = len(scores)
    assert 4 <= n <= 5 * 10**4, "4 <= n <= 5 * 10^4"
    assert all(1 <= v <= 10**8 for v in scores), "1 <= scores[i] <= 10^8"
    assert 0 <= len(edges) <= 5 * 10**4, "0 <= edges.length <= 5 * 10^4"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b in edges), "0 <= ai, bi <= n - 1"
    assert all(a != b for a, b in edges), "ai != bi"
    seen = {(min(a, b), max(a, b)) for a, b in edges}
    assert len(seen) == len(edges), "There are no duplicate edges"
