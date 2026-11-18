"""Rearrange Words in a Sentence: a capitalized sentence of lowercase words."""


def check(text: str) -> None:
    assert 1 <= len(text) <= 10**5, "1 <= text.length <= 10^5"
    assert "A" <= text[0] <= "Z", "text begins with a capital letter"
    assert all("a" <= c <= "z" or c == " " for c in text[1:]), "then lowercase letters and spaces"
    assert "  " not in text, "single space between words"
