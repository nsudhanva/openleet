"""Check If a Word Occurs As a Prefix of Any Word in a Sentence: a sentence and a search word."""


def check(sentence: str, searchWord: str) -> None:
    assert isinstance(sentence, str) and isinstance(searchWord, str), "both are strings"
    assert 1 <= len(sentence) <= 100, "1 <= sentence.length <= 100"
    assert 1 <= len(searchWord) <= 10, "1 <= searchWord.length <= 10"
    assert all(c == " " or "a" <= c <= "z" for c in sentence), (
        "sentence consists of lowercase English letters and spaces"
    )
    assert all("a" <= c <= "z" for c in searchWord), (
        "searchWord consists of lowercase English letters"
    )
