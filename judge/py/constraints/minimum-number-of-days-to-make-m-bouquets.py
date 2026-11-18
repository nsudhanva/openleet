"""Minimum Number of Days to Make m Bouquets: bloom days plus bouquet count m and flowers per
bouquet k."""


def check(bloomDay: list[int], m: int, k: int) -> None:
    assert isinstance(bloomDay, list), "bloomDay is an array"
    n = len(bloomDay)
    assert 1 <= n <= 10**5, "1 <= n <= 10^5"
    assert all(isinstance(v, int) and 1 <= v <= 10**9 for v in bloomDay), "1 <= bloomDay[i] <= 10^9"
    assert isinstance(m, int) and 1 <= m <= 10**6, "1 <= m <= 10^6"
    assert isinstance(k, int) and 1 <= k <= n, "1 <= k <= n"
