"""Verbal Arithmetic Puzzle: 2 to 5 uppercase words and an uppercase result word."""


def check(words: list[str], result: str) -> None:
    assert 2 <= len(words) <= 5, "2 <= words.length <= 5"
    assert all(1 <= len(w) <= 7 for w in words), "1 <= words[i].length <= 7"
    assert 1 <= len(result) <= 7, "1 <= result.length <= 7"
    assert all(w.isascii() and w.isalpha() and w.isupper() for w in [*words, result]), (
        "words[i], result contain only uppercase English letters"
    )
    assert len(set("".join(words) + result)) <= 10, "at most 10 different characters"
