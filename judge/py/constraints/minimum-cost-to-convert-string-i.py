"""Minimum Cost to Convert String I: source and target strings with letter-change costs."""


def check(
    source: str, target: str, original: list[str], changed: list[str], cost: list[int]
) -> None:
    assert isinstance(source, str) and isinstance(target, str), "source and target are strings"
    assert 1 <= len(source) <= 10**5, "1 <= source.length <= 10^5"
    assert len(source) == len(target), "source.length == target.length"
    assert all("a" <= c <= "z" for c in source + target), (
        "source, target consist of lowercase English letters"
    )
    assert 1 <= len(cost) <= 2000, "1 <= cost.length <= 2000"
    assert len(cost) == len(original) == len(changed), (
        "cost.length == original.length == changed.length"
    )
    letters = all(
        isinstance(c, str) and len(c) == 1 and "a" <= c <= "z" for c in original + changed
    )
    assert letters, "original[i], changed[i] are lowercase English letters"
    assert all(1 <= c <= 10**6 for c in cost), "1 <= cost[i] <= 10^6"
    assert all(a != b for a, b in zip(original, changed, strict=True)), "original[i] != changed[i]"
