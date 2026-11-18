"""Word Squares: a list of distinct same-length lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    assert all(1 <= len(w) <= 4 for w in words), "1 <= words[i].length <= 4"
    assert len({len(w) for w in words}) == 1, "all words[i] have the same length"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists of only lowercase English letters"
    )
    assert len(set(words)) == len(words), "all words[i] are unique"
