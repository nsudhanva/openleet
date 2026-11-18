"""Number of Islands II: grid dimensions and a list of [row, col] land positions."""


def check(m: int, n: int, positions: list[list[int]]) -> None:
    assert 1 <= m <= 10**4, "1 <= m <= 10^4"
    assert 1 <= n <= 10**4, "1 <= n <= 10^4"
    assert 1 <= len(positions) <= 10**4, "1 <= positions.length <= 10^4"
    assert 1 <= m * n <= 10**4, "1 <= m * n <= 10^4"
    assert all(len(p) == 2 for p in positions), "positions[i].length == 2"
    assert all(0 <= r < m for r, _ in positions), "0 <= ri < m"
    assert all(0 <= c < n for _, c in positions), "0 <= ci < n"
