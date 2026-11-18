"""Couples Holding Hands: a row of 2n distinct seat ids forming a permutation of 0..2n-1."""


def check(row: list[int]) -> None:
    assert len(row) % 2 == 0, "2n == row.length"
    n = len(row) // 2
    assert 2 <= n <= 30, "2 <= n <= 30"
    assert all(0 <= v < 2 * n for v in row), "0 <= row[i] < 2n"
    assert len(set(row)) == len(row), "all the elements of row are unique"
