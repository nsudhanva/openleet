"""Index Pairs of a String: a text and a list of unique words."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(text: str, words: list[str]) -> None:
    assert 1 <= len(text) <= 100, "1 <= text.length <= 100"
    assert 1 <= len(words) <= 20, "1 <= words.length <= 20"
    assert all(1 <= len(w) <= 50 for w in words), "1 <= words[i].length <= 50"
    assert set(text) <= LOWER, "text consists of lowercase English letters"
    assert all(set(w) <= LOWER for w in words), "words[i] consist of lowercase English letters"
    assert len(set(words)) == len(words), "All the strings of words are unique"
