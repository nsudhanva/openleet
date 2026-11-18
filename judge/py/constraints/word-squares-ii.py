"""Word Squares II: a list of distinct four-letter lowercase words."""


def check(words: list[str]) -> None:
    assert 4 <= len(words) <= 15, "4 <= words.length <= 15"
    assert all(len(w) == 4 for w in words), "words[i].length == 4"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists of only lowercase English letters"
    )
    assert len(set(words)) == len(words), "all words[i] are distinct"
