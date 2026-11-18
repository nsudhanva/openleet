"""Number of Matching Subsequences: a lowercase string and a list of lowercase words."""


def check(s: str, words: list[str]) -> None:
    assert 1 <= len(s) <= 5 * 10**4, "1 <= s.length <= 5 * 10^4"
    assert 1 <= len(words) <= 5000, "1 <= words.length <= 5000"
    assert all(1 <= len(w) <= 50 for w in words), "1 <= words[i].length <= 50"
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consist of only lowercase English letters"
    )
