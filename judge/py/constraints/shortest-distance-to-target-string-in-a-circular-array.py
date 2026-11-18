"""Shortest Distance to Target String in a Circular Array: words, a target and a start index."""


def check(words: list[str], target: str, startIndex: int) -> None:
    assert 1 <= len(words) <= 100, "1 <= words.length <= 100"
    assert all(1 <= len(w) <= 100 for w in words), "1 <= words[i].length <= 100"
    assert all("a" <= ch <= "z" for w in words for ch in w), (
        "words[i] consists of only lowercase English letters"
    )
    assert all("a" <= ch <= "z" for ch in target), (
        "target consists of only lowercase English letters"
    )
    assert 0 <= startIndex < len(words), "0 <= startIndex < words.length"
