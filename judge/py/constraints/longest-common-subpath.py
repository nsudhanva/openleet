"""Longest Common Subpath: n cities and m paths over them."""


def check(n: int, paths: list[list[int]]) -> None:
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert 2 <= len(paths) <= 10**5, "2 <= m <= 10^5"
    assert sum(len(p) for p in paths) <= 10**5, "sum(paths[i].length) <= 10^5"
    for p in paths:
        assert all(0 <= v < n for v in p), "0 <= paths[i][j] < n"
        assert all(p[i] != p[i + 1] for i in range(len(p) - 1)), (
            "the same city is not listed multiple times consecutively in paths[i]"
        )
