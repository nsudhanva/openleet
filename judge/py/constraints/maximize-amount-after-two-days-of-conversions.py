"""Maximize Amount After Two Days of Conversions: a start currency and two days of rates."""

import string


def _currency(c: str) -> bool:
    return isinstance(c, str) and 1 <= len(c) <= 3 and all(ch in string.ascii_uppercase for ch in c)


def _acyclic(pairs: list[list[str]]) -> bool:
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True


def check(
    initialCurrency: str,
    pairs1: list[list[str]],
    rates1: list[float],
    pairs2: list[list[str]],
    rates2: list[float],
) -> None:
    assert _currency(initialCurrency), "initialCurrency is 1 to 3 uppercase English letters"
    assert 1 <= len(pairs1) <= 10, "1 <= n == pairs1.length <= 10"
    assert 1 <= len(pairs2) <= 10, "1 <= m == pairs2.length <= 10"
    for pairs in (pairs1, pairs2):
        assert all(len(p) == 2 for p in pairs), "pairs[i] == [startCurrency, targetCurrency]"
        assert all(_currency(c) for p in pairs for c in p), (
            "currencies are 1 to 3 uppercase English letters"
        )
    assert len(rates1) == len(pairs1), "rates1.length == n"
    assert len(rates2) == len(pairs2), "rates2.length == m"
    assert all(1.0 <= r <= 10.0 for r in rates1 + rates2), "1.0 <= rates[i] <= 10.0"
    assert _acyclic(pairs1), "no contradictions or cycles in the day 1 conversion graph"
    assert _acyclic(pairs2), "no contradictions or cycles in the day 2 conversion graph"
