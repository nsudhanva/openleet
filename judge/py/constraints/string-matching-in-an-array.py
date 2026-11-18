"""String Matching in an Array: a list of unique lowercase words."""


def check(words: list[str]) -> None:
    assert isinstance(words, list), "words is a list"
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    for w in words:
        assert isinstance(w, str) and 1 <= len(w) <= 30, "1 <= words[i].length <= 30"
        assert all("a" <= c <= "z" for c in w), "words[i] contains only lowercase English letters"
    assert len(set(words)) == len(words), "all the strings of words are unique"
