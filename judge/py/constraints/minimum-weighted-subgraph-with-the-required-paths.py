"""Minimum Weighted Subgraph With the Required Paths: a weighted digraph and three nodes."""


def check(n: int, edges: list[list[int]], src1: int, src2: int, dest: int) -> None:
    assert 3 <= n <= 10**5, "3 <= n <= 10^5"
    assert 0 <= len(edges) <= 10**5, "0 <= edges.length <= 10^5"
    assert all(len(e) == 3 for e in edges), "edges[i].length == 3"
    assert all(0 <= a <= n - 1 and 0 <= b <= n - 1 for a, b, _ in edges), "0 <= fromi, toi <= n - 1"
    assert all(0 <= x <= n - 1 for x in (src1, src2, dest)), "0 <= src1, src2, dest <= n - 1"
    assert all(a != b for a, b, _ in edges), "fromi != toi"
    assert len({src1, src2, dest}) == 3, "src1, src2, and dest are pairwise distinct"
    assert all(1 <= w <= 10**5 for _, _, w in edges), "1 <= weight[i] <= 10^5"
