"""Split Strings by Separator: words and a one-character separator."""

SEPS = ".,|$#@"


def check(words: list[str], separator: str) -> None:
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(isinstance(w, str) for w in words), "words[i] is a string"
    assert all(1 <= len(w) <= 20 for w in words), "1 <= words[i].length <= 20"
    assert all(c in SEPS or "a" <= c <= "z" for w in words for c in w), (
        'characters in words[i] are lowercase letters or from ".,|$#@"'
    )
    assert isinstance(separator, str) and len(separator) == 1 and separator in SEPS, (
        'separator is a character from ".,|$#@"'
    )
