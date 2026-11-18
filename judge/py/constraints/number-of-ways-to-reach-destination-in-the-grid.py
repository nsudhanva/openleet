"""Number of Ways to Reach Destination in the Grid: an n x m grid, k moves, source and dest
cells."""


def check(n: int, m: int, k: int, source: list[int], dest: list[int]) -> None:
    assert 2 <= n <= 10**9, "2 <= n <= 10^9"
    assert 2 <= m <= 10**9, "2 <= m <= 10^9"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
    assert len(source) == len(dest) == 2, "source.length == dest.length == 2"
    assert 1 <= source[0] <= n and 1 <= dest[0] <= n, "row of source and dest in 1..n"
    assert 1 <= source[1] <= m and 1 <= dest[1] <= m, "column of source and dest in 1..m"
