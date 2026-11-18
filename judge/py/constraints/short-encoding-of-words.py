"""Short Encoding of Words: a list of short lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 2000, "1 <= words.length <= 2000"
    assert all(1 <= len(w) <= 7 for w in words), "1 <= words[i].length <= 7"
    assert all("a" <= ch <= "z" for w in words for ch in w), (
        "words[i] consists of only lowercase letters"
    )
