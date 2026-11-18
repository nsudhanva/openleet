"""Longest Uncommon Subsequence I: two lowercase strings."""


def check(a: str, b: str) -> None:
    for name, t in (("a", a), ("b", b)):
        assert 1 <= len(t) <= 100, f"1 <= {name}.length <= 100"
        assert all(c.isascii() and c.isalpha() and c.islower() for c in t), (
            f"{name} consists of lower-case English letters"
        )
