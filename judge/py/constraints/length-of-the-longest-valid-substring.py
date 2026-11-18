"""Length of the Longest Valid Substring: a word and a list of forbidden strings."""


def check(word: str, forbidden: list[str]) -> None:
    assert 1 <= len(word) <= 10**5, "1 <= word.length <= 10^5"
    assert all("a" <= c <= "z" for c in word), "word consists only of lowercase English letters"
    assert 1 <= len(forbidden) <= 10**5, "1 <= forbidden.length <= 10^5"
    assert all(1 <= len(f) <= 10 for f in forbidden), "1 <= forbidden[i].length <= 10"
    assert all("a" <= c <= "z" for f in forbidden for c in f), (
        "forbidden[i] consists only of lowercase English letters"
    )
