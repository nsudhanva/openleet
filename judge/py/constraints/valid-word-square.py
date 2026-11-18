"""Valid Word Square: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 500, "1 <= words.length <= 500"
    assert all(1 <= len(w) <= 500 for w in words), "1 <= words[i].length <= 500"
    assert all(w.isascii() and w.isalpha() and w.islower() for w in words), (
        "words[i] consists of only lowercase English letters"
    )
