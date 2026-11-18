"""Check if the Sentence Is Pangram: a lowercase string."""

LOWER = set("abcdefghijklmnopqrstuvwxyz")


def check(sentence: str) -> None:
    assert 1 <= len(sentence) <= 1000, "1 <= sentence.length <= 1000"
    assert set(sentence) <= LOWER, "sentence consists of lowercase English letters"
