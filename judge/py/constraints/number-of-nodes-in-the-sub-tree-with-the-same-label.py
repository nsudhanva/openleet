"""Number of Nodes in the Sub-Tree With the Same Label: a tree with a label per node."""


def check(n: int, edges: list[list[int]], labels: str) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(edges) == n - 1, "edges.length == n - 1"
    assert all(len(e) == 2 for e in edges), "edges[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= ai, bi < n"
    assert all(a != b for a, b in edges), "ai != bi"
    assert len(labels) == n, "labels.length == n"
    assert all("a" <= c <= "z" for c in labels), "labels consists of only lowercase English letters"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, "the edges form a tree"
        parent[ra] = rb
