"""Similar String Groups: lowercase anagrams of equal length."""


def check(strs: list[str]) -> None:
    assert 1 <= len(strs) <= 300, "1 <= strs.length <= 300"
    assert all(isinstance(s, str) for s in strs), "strs[i] is a string"
    n = len(strs[0])
    assert 1 <= n <= 300, "1 <= strs[i].length <= 300"
    assert all(len(s) == n for s in strs), "all words in strs have the same length"
    assert all(s.isascii() and s.isalpha() and s.islower() for s in strs), (
        "strs[i] consists of lowercase letters only"
    )
    key = sorted(strs[0])
    assert all(sorted(s) == key for s in strs), "all words in strs are anagrams of each other"
