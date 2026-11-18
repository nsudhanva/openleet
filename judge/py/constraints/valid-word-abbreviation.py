"""Valid Word Abbreviation: a lowercase word and an abbreviation of letters and digits."""

import re


def check(word: str, abbr: str) -> None:
    assert 1 <= len(word) <= 20, "1 <= word.length <= 20"
    assert word.isascii() and word.islower() and word.isalpha(), (
        "word consists of only lowercase English letters"
    )
    assert 1 <= len(abbr) <= 10, "1 <= abbr.length <= 10"
    assert all(c.isascii() and (c.islower() or c.isdigit()) for c in abbr), (
        "abbr consists of lowercase English letters and digits"
    )
    assert all(int(m) < 2**31 for m in re.findall(r"\d+", abbr)), (
        "all the integers in abbr fit in a 32-bit integer"
    )
