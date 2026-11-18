"""Number of Laser Beams in a Bank: rows of '0'/'1' strings of equal length."""


def check(bank: list[str]) -> None:
    m = len(bank)
    assert 1 <= m <= 500, "1 <= m <= 500"
    n = len(bank[0])
    assert all(len(row) == n for row in bank), "n == bank[i].length"
    assert 1 <= n <= 500, "1 <= n <= 500"
    assert all(c in ("0", "1") for row in bank for c in row), "bank[i][j] is either '0' or '1'"
