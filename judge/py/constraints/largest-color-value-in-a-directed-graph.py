"""Largest Color Value in a Directed Graph: node colors and directed edges."""


def check(colors: str, edges: list[list[int]]) -> None:
    n = len(colors)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert len(edges) <= 10**5, "0 <= m <= 10^5"
    assert all(c in "abcdefghijklmnopqrstuvwxyz" for c in colors), (
        "colors consists of lowercase English letters"
    )
    assert all(len(e) == 2 for e in edges), "edges[j].length == 2"
    assert all(0 <= a < n and 0 <= b < n for a, b in edges), "0 <= aj, bj < n"
