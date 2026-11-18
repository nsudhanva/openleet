"""Truncate Sentence: a sentence of single-space separated words and a word count k."""


def check(s: str, k: int) -> None:
    assert 1 <= len(s) <= 500, "1 <= s.length <= 500"
    assert all(c == " " or ("a" <= c <= "z") or ("A" <= c <= "Z") for c in s), (
        "s consists of only lowercase and uppercase English letters and spaces"
    )
    assert not s.startswith(" ") and not s.endswith(" "), "no leading or trailing spaces"
    assert "  " not in s, "words are separated by a single space"
    assert 1 <= k <= len(s.split(" ")), "k is in the range [1, the number of words in s]"
