"""Count Prefix and Suffix Pairs II: lowercase words with bounded total length."""


def check(words: list[str]) -> None:
    assert 1 <= len(words) <= 10**5, "1 <= words.length <= 10^5"
    assert all(1 <= len(w) <= 10**5 for w in words), "1 <= words[i].length <= 10^5"
    assert all("a" <= c <= "z" for w in words for c in w), (
        "words[i] consists only of lowercase English letters"
    )
    assert sum(len(w) for w in words) <= 5 * 10**5, "sum of words[i].length <= 5 * 10^5"
