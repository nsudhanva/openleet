"""Check If String Is a Prefix of Array: a lowercase string and a list of lowercase words."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(s: str, words: list[str]) -> None:
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(1 <= len(w) <= 20 for w in words), "1 <= words[i].length <= 20"
    assert 1 <= len(s) <= 1000, "1 <= s.length <= 1000"
    assert all(set(w) <= LOWER for w in words) and set(s) <= LOWER, (
        "words[i] and s consist of only lowercase English letters"
    )
