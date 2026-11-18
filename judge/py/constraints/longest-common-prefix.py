"""Longest Common Prefix: a list of lowercase strings, possibly empty."""


def check(strs: list[str]) -> None:
    assert 1 <= len(strs) <= 200, "1 <= strs.length <= 200"
    assert all(isinstance(t, str) for t in strs), "strs[i] is a string"
    assert all(0 <= len(t) <= 200 for t in strs), "0 <= strs[i].length <= 200"
    assert all("a" <= c <= "z" for t in strs for c in t), (
        "strs[i] consists of only lowercase English letters if it is non-empty"
    )
