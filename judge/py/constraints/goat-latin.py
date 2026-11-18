"""Goat Latin: a sentence of English words separated by single spaces."""


def check(sentence: str) -> None:
    assert 1 <= len(sentence) <= 150, "1 <= sentence.length <= 150"
    assert all(c == " " or ("a" <= c <= "z") or ("A" <= c <= "Z") for c in sentence), (
        "sentence consists of English letters and spaces"
    )
    assert sentence == sentence.strip(" "), "no leading or trailing spaces"
    assert "  " not in sentence, "words are separated by a single space"
