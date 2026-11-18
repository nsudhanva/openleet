"""Find Resultant Array After Removing Anagrams: a list of lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(isinstance(w, str) and 1 <= len(w) <= 10 for w in words), (
        "1 <= words[i].length <= 10"
    )
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consists of lowercase English letters"
    )
