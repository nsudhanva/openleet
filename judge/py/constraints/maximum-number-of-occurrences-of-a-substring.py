"""Maximum Number of Occurrences of a Substring: a lowercase string and size/letter limits."""


def check(s: str, maxLetters: int, minSize: int, maxSize: int) -> None:
    assert 1 <= len(s) <= 10**5, "1 <= s.length <= 10^5"
    assert all("a" <= c <= "z" for c in s), "s consists of only lowercase English letters"
    assert 1 <= maxLetters <= 26, "1 <= maxLetters <= 26"
    assert 1 <= minSize <= maxSize <= min(26, len(s)), (
        "1 <= minSize <= maxSize <= min(26, s.length)"
    )
