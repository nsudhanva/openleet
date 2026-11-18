"""Minimum Cost to Separate Sentence into Rows: a sentence of lowercase words and a row width k."""


def check(sentence: str, k: int) -> None:
    assert isinstance(sentence, str), "sentence is a string"
    assert 1 <= len(sentence) <= 5000, "1 <= sentence.length <= 5000"
    assert 1 <= k <= 5000, "1 <= k <= 5000"
    assert all(c == " " or "a" <= c <= "z" for c in sentence), (
        "sentence has only lowercase letters and spaces"
    )
    assert sentence[0] != " " and sentence[-1] != " ", "sentence does not begin or end with a space"
    assert "  " not in sentence, "words are separated by a single space"
    assert all(len(w) <= k for w in sentence.split(" ")), "the length of each word is at most k"
