"""Groups of Special-Equivalent Strings: an array of equal-length lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 1000, "1 <= words.length <= 1000"
    assert all(1 <= len(w) <= 20 for w in words), "1 <= words[i].length <= 20"
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consist of lowercase English letters"
    )
    assert len({len(w) for w in words}) == 1, "all the strings are of the same length"
