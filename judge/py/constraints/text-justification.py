"""Text Justification: a list of words and a line width."""


def check(words: list[str], maxWidth: int) -> None:
    assert 1 <= len(words) <= 300, "1 <= words.length <= 300"
    assert all(isinstance(w, str) and 1 <= len(w) <= 20 for w in words), (
        "1 <= words[i].length <= 20"
    )
    assert all(" " not in w for w in words), "a word consists of non-space characters only"
    assert 1 <= maxWidth <= 100, "1 <= maxWidth <= 100"
    assert all(len(w) <= maxWidth for w in words), "words[i].length <= maxWidth"
