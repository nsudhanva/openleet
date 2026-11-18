"""Word Break: a lowercase string and a dictionary of distinct lowercase words."""


def _lower(s: str) -> bool:
    return s.isascii() and s.isalpha() and s.islower()


def check(s: str, wordDict: list[str]) -> None:
    assert 1 <= len(s) <= 300, "1 <= s.length <= 300"
    assert 1 <= len(wordDict) <= 1000, "1 <= wordDict.length <= 1000"
    assert all(1 <= len(w) <= 20 for w in wordDict), "1 <= wordDict[i].length <= 20"
    assert _lower(s), "s consists of only lowercase English letters"
    assert all(_lower(w) for w in wordDict), (
        "wordDict[i] consists of only lowercase English letters"
    )
    assert len(set(wordDict)) == len(wordDict), "all the strings of wordDict are unique"
