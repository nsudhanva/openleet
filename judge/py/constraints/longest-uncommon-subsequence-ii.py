"""Longest Uncommon Subsequence II: a list of lowercase strings."""


def check(strs: list[str]) -> None:
    assert 2 <= len(strs) <= 50, "2 <= strs.length <= 50"
    assert all(1 <= len(t) <= 10 for t in strs), "1 <= strs[i].length <= 10"
    assert all(t.isascii() and t.isalpha() and t.islower() for t in strs), (
        "strs[i] consists of lowercase English letters"
    )
