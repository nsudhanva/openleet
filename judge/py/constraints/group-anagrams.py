"""Group Anagrams: an array of lowercase strings."""


def check(strs: list[str]) -> None:
    assert 1 <= len(strs) <= 10**4, "1 <= strs.length <= 10^4"
    assert all(0 <= len(s) <= 100 for s in strs), "0 <= strs[i].length <= 100"
    assert all("a" <= c <= "z" for s in strs for c in s), (
        "strs[i] consists of lowercase English letters"
    )
