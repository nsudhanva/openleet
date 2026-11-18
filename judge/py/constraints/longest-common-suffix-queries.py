"""Longest Common Suffix Queries: two lists of lowercase words."""


def check(wordsContainer: list[str], wordsQuery: list[str]) -> None:
    assert 1 <= len(wordsContainer) <= 10**4, "1 <= wordsContainer.length <= 10^4"
    assert 1 <= len(wordsQuery) <= 10**4, "1 <= wordsQuery.length <= 10^4"
    for name, words in (("wordsContainer", wordsContainer), ("wordsQuery", wordsQuery)):
        assert all(isinstance(w, str) for w in words), f"{name}[i] is a string"
        assert all(1 <= len(w) <= 5 * 10**3 for w in words), f"1 <= {name}[i].length <= 5 * 10^3"
        assert all(w.isascii() and w.islower() and w.isalpha() for w in words), (
            f"{name}[i] consists only of lowercase English letters"
        )
        assert sum(map(len, words)) <= 5 * 10**5, f"Sum of {name}[i].length <= 5 * 10^5"
