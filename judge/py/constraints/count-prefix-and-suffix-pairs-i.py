"""Count Prefix and Suffix Pairs I: a few short lowercase words."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 50, "1 <= words.length <= 50"
    assert all(1 <= len(w) <= 10 for w in words), "1 <= words[i].length <= 10"
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consists only of lowercase English letters"
    )
