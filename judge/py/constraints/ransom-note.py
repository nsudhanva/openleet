"""Ransom Note: two lowercase strings."""


def check(ransomNote: str, magazine: str) -> None:
    assert 1 <= len(ransomNote) <= 10**5, "1 <= ransomNote.length <= 10^5"
    assert 1 <= len(magazine) <= 10**5, "1 <= magazine.length <= 10^5"
    for s in (ransomNote, magazine):
        assert all("a" <= c <= "z" for c in s), "lowercase English letters"
