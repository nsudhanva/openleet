"""Number of Valid Words in a Sentence: a sentence of letters, digits, spaces, punctuation."""


def check(sentence: str) -> None:
    assert isinstance(sentence, str), "sentence is a string"
    assert 1 <= len(sentence) <= 1000, "1 <= sentence.length <= 1000"
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789 -!.,")
    assert set(sentence) <= allowed, "only lowercase letters, digits, ' ', '-', '!', '.', ','"
    assert sentence.split(), "at least 1 token"
