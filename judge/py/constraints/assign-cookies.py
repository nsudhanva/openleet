"""Assign Cookies: children's greed factors g and cookie sizes s."""


def check(g: list[int], s: list[int]) -> None:
    assert 1 <= len(g) <= 3 * 10**4, "1 <= g.length <= 3 * 10^4"
    assert 0 <= len(s) <= 3 * 10**4, "0 <= s.length <= 3 * 10^4"
    assert all(1 <= v <= 2**31 - 1 for v in g), "1 <= g[i] <= 2^31 - 1"
    assert all(1 <= v <= 2**31 - 1 for v in s), "1 <= s[j] <= 2^31 - 1"
