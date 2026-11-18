"""Find Common Characters: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(1 <= len(w) <= 100 for w in words), "1 <= words[i].length <= 100"
    assert all(w.isascii() and w.islower() and w.isalpha() for w in words), (
        "words[i] consists of lowercase English letters"
    )
