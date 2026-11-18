"""Find Minimum Diameter After Merging Two Trees: the edge lists of two trees on 0..n-1 and
0..m-1."""


def _check_tree(name: str, edges: list[list[int]]) -> None:
    n = len(edges) + 1
    assert 1 <= n <= 10**5, f"1 <= n <= 10^5 ({name})"
    assert all(len(e) == 2 for e in edges), f"{name}[i].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), f"0 <= endpoints < n ({name})"
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        assert ra != rb, f"{name} represents a valid tree"
        parent[ra] = rb


def check(edges1: list[list[int]], edges2: list[list[int]]) -> None:
    _check_tree("edges1", edges1)
    _check_tree("edges2", edges2)
