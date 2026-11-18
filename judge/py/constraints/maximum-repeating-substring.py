"""Maximum Repeating Substring: a sequence and a word, both lowercase."""


def check(sequence: str, word: str) -> None:
    assert 1 <= len(sequence) <= 100, "1 <= sequence.length <= 100"
    assert 1 <= len(word) <= 100, "1 <= word.length <= 100"
    assert all("a" <= c <= "z" for c in sequence), (
        "sequence contains only lowercase English letters"
    )
    assert all("a" <= c <= "z" for c in word), "word contains only lowercase English letters"
