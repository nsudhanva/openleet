"""Find Beautiful Indices in the Given Array I: strings s, a, b and a distance k."""


def _lower(t: str) -> bool:
    return isinstance(t, str) and t.isascii() and t.islower() and t.isalpha()


def check(s: str, a: str, b: str, k: int) -> None:
    assert _lower(s) and _lower(a) and _lower(b), (
        "s, a, and b contain only lowercase English letters"
    )
    assert 1 <= k <= len(s) <= 10**5, "1 <= k <= s.length <= 10^5"
    assert 1 <= len(a) <= 10 and 1 <= len(b) <= 10, "1 <= a.length, b.length <= 10"
