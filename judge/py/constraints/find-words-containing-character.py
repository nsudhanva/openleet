"""Find Words Containing Character: a list of lowercase words and a lowercase letter."""


def check(words: list[str], x: str) -> None:
    assert 1 <= len(words) <= 50, "1 <= words.length <= 50"
    assert all(1 <= len(w) <= 50 for w in words), "1 <= words[i].length <= 50"
    assert len(x) == 1 and "a" <= x <= "z", "x is a lowercase English letter"
    assert all(c.isascii() and c.islower() for w in words for c in w), (
        "words[i] consists only of lowercase English letters"
    )
