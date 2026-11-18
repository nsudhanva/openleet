"""Longest Substring of One Repeating Character: a string and character-update queries."""


def check(s: str, queryCharacters: str, queryIndices: list[int]) -> None:
    def lower(t: str) -> bool:
        return all(c.isascii() and c.isalpha() and c.islower() for c in t)

    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert lower(s), "s consists of lowercase English letters"
    k = len(queryCharacters)
    assert k == len(queryIndices), "k == queryCharacters.length == queryIndices.length"
    assert 1 <= k <= 10**5, "1 <= k <= 10^5"
    assert lower(queryCharacters), "queryCharacters consists of lowercase English letters"
    assert all(0 <= i < len(s) for i in queryIndices), "0 <= queryIndices[i] < s.length"
