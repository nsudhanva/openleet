"""Sentence Screen Fitting: a list of lowercase words plus screen rows and cols."""

import string


def check(sentence: list[str], rows: int, cols: int) -> None:
    assert 1 <= len(sentence) <= 100, "1 <= sentence.length <= 100"
    assert all(1 <= len(w) <= 10 for w in sentence), "1 <= sentence[i].length <= 10"
    assert all(set(w) <= set(string.ascii_lowercase) for w in sentence), (
        "sentence[i] consists of lowercase English letters"
    )
    assert 1 <= rows <= 2 * 10**4 and 1 <= cols <= 2 * 10**4, "1 <= rows, cols <= 2 * 10^4"
