"""Word Abbreviation: a list of distinct lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 400, "1 <= words.length <= 400"
    assert all(2 <= len(w) <= 400 for w in words), "2 <= words[i].length <= 400"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists of lowercase English letters"
    )
    assert len(set(words)) == len(words), "all the strings of words are unique"
