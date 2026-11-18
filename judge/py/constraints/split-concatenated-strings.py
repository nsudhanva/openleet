"""Split Concatenated Strings: a list of lowercase strings."""


def check(strs: list[str]) -> None:
    assert 1 <= len(strs) <= 1000, "1 <= strs.length <= 1000"
    assert all(isinstance(s, str) for s in strs), "strs[i] is a string"
    assert all(1 <= len(s) <= 1000 for s in strs), "1 <= strs[i].length <= 1000"
    assert 1 <= sum(len(s) for s in strs) <= 1000, "1 <= sum(strs[i].length) <= 1000"
    assert all("a" <= c <= "z" for s in strs for c in s), (
        "strs[i] consists of lowercase English letters"
    )
