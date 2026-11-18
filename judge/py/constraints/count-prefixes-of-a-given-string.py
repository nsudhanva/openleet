"""Count Prefixes of a Given String: lowercase words and a string s."""


def check(words: list[str], s: str) -> None:
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    assert all(1 <= len(w) <= 10 for w in words), "1 <= words[i].length <= 10"
    assert 1 <= len(s) <= 10, "1 <= s.length <= 10"
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consists of lowercase English letters only"
    )
    assert all("a" <= c <= "z" for c in s), "s consists of lowercase English letters only"
