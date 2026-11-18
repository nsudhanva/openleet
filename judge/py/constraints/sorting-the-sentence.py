"""Sorting the Sentence: a shuffled sentence whose words end in their position 1-9."""


def check(s: str) -> None:
    assert 2 <= len(s) <= 200, "2 <= s.length <= 200"
    assert all(c.isascii() and (c.isalnum() or c == " ") for c in s), (
        "s consists of letters, spaces and digits"
    )
    assert "0" not in s, "digits are from 1 to 9"
    words = s.split(" ")
    assert 1 <= len(words) <= 9, "the number of words in s is between 1 and 9"
    assert all(words), "words are separated by a single space, no leading or trailing spaces"
    assert all(w[:-1].isalpha() and w[:-1].isascii() for w in words), (
        "each word is English letters followed by its 1-indexed position"
    )
    assert sorted(w[-1] for w in words) == [str(i) for i in range(1, len(words) + 1)], (
        "the appended positions are 1..number of words, each once"
    )
