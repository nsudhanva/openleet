"""Rearrange Spaces Between Words: text of lowercase letters and spaces with a word."""


def check(text: str) -> None:
    assert 1 <= len(text) <= 100, "1 <= text.length <= 100"
    assert all(c == " " or "a" <= c <= "z" for c in text), "lowercase English letters and ' '"
    assert text.strip(" ") != "", "text contains at least one word"
