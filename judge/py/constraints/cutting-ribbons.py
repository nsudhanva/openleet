"""Cutting Ribbons: ribbon lengths and the number k of equal pieces wanted."""


def check(ribbons: list[int], k: int) -> None:
    assert 1 <= len(ribbons) <= 10**5, "1 <= ribbons.length <= 10^5"
    assert all(1 <= r <= 10**5 for r in ribbons), "1 <= ribbons[i] <= 10^5"
    assert 1 <= k <= 10**9, "1 <= k <= 10^9"
