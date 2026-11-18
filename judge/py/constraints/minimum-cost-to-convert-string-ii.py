"""Minimum Cost to Convert String II: two equal-length strings and a list of substring rewrites."""


def check(
    source: str, target: str, original: list[str], changed: list[str], cost: list[int]
) -> None:
    assert isinstance(source, str) and isinstance(target, str), "source, target are strings"
    assert len(source) == len(target), "source.length == target.length"
    assert 1 <= len(source) <= 1000, "1 <= source.length <= 1000"
    for t in (source, target):
        assert all("a" <= c <= "z" for c in t), "source, target are lowercase English letters"
    assert len(cost) == len(original) == len(changed), (
        "cost.length == original.length == changed.length"
    )
    assert 1 <= len(cost) <= 100, "1 <= cost.length <= 100"
    for o, c in zip(original, changed, strict=True):
        assert isinstance(o, str) and isinstance(c, str), "original[i], changed[i] are strings"
        assert len(o) == len(c), "original[i].length == changed[i].length"
        assert 1 <= len(o) <= len(source), "1 <= original[i].length <= source.length"
        assert all("a" <= x <= "z" for x in o + c), (
            "original[i], changed[i] are lowercase English letters"
        )
        assert o != c, "original[i] != changed[i]"
    assert all(1 <= x <= 10**6 for x in cost), "1 <= cost[i] <= 10^6"
