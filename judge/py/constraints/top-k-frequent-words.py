"""Top K Frequent Words: lowercase words and k."""


def check(words: list[str], k: int) -> None:
    assert 1 <= len(words) <= 500, "1 <= words.length <= 500"
    assert all(isinstance(w, str) and 1 <= len(w) <= 10 for w in words), (
        "1 <= words[i].length <= 10"
    )
    assert all(c in "abcdefghijklmnopqrstuvwxyz" for w in words for c in w), (
        "words[i] consists of lowercase English letters"
    )
    assert 1 <= k <= len(set(words)), "k is in the range [1, the number of unique words[i]]"
